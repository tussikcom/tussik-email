import logging
import re
import smtplib
import ssl
from email.headerregistry import Address
from email.message import EmailMessage
from typing import Optional, Union, List

from tld import is_tld

logger = logging.getLogger("tussik.email")


def _extract_emails(s: str, multiple: bool = True, as_array: bool = False) -> Union[str, List[str]]:
    parts = re.split(';|,| ', str(s))
    parts = [str(item).strip().lower() for item in parts]
    parts = [item for item in parts if item.count("@") == 1 and "." in item]

    emails = []
    for item in parts:
        tld = item.split(".")[-1]
        if not is_tld(tld):
            continue
        n = item.index("@")
        if n > 0 and n < len(item):
            emails.append(item)
            if not multiple:
                break
    emails = list(set(emails))

    if as_array:
        return emails
    if len(emails) == 0:
        return ""
    return ", ".join(emails)


class Email:
    __slots__ = ['__to', '__cc', '__bcc', '__replyto', '__sender', '__errormsg',
                 '__subject', '__html', '__text', '__attach', '__headers', '__headers_raw',
                 '__host', '__port', '__username', '__password']

    def __init__(self, host: Optional[str] = None,
                 port: Optional[int] = None,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        self.__host: Optional[str] = host
        self.__port: Optional[int] = port
        self.__username: Optional[str] = username
        self.__password: Optional[str] = password
        self.__to = list()
        self.__cc = list()
        self.__bcc = list()
        self.__replyto = None
        self.__sender = None
        self.__subject = ""
        self.__html = None
        self.__text = None
        self.__attach = list()
        self.__headers: dict = {}
        self.__headers_raw: dict = {}
        self.__errormsg: Optional[str] = None

    def __address(self, address: str, name: Optional[str] = None):
        addr = address.split('@')
        if name is None:
            return Address(addr[0], addr[0], addr[1])
        else:
            return Address(name, addr[0], addr[1])

    def clear_to(self):
        self.__to = list()

    def clear_cc(self):
        self.__cc = list()

    def clear_bcc(self):
        self.__bcc = list()

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def errormsg(self) -> Optional[str]:
        return self.__errormsg

    @subject.setter
    def subject(self, line: str):
        self.__subject = line

    def sender(self, address: str, name: Optional[str] = None):
        self.__sender = self.__address(address, name)

    def replyto(self, address: str):
        self.__replyto = str(address).strip()

    def to(self, address: str, name: Optional[str] = None):
        for email in _extract_emails(address, multiple=True, as_array=True):
            self.__to.append(self.__address(email, name))

    def cc(self, address: str, name: Optional[str] = None):
        for email in _extract_emails(address, multiple=True, as_array=True):
            self.__cc.append(self.__address(email, name))

    def bcc(self, address: str, name: Optional[str] = None):
        for email in _extract_emails(address, multiple=True, as_array=True):
            self.__bcc.append(self.__address(email, name))

    def references(self, val: str):
        if "References" in self.__headers_raw:
            self.__headers_raw["References"] += f" <{val}>"
        else:
            self.__headers_raw["References"] = f"<{val}>"

    def header(self, key: str, val: str, raw: bool = False):
        if raw:
            self.__headers_raw[key] = val
        else:
            self.__headers[key.upper()] = val

    @property
    def html(self) -> str:
        return self.__html

    @html.setter
    def html(self, html: str):
        self.__html = html

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    def clear_attachments(self):
        self.__attach = list()

    def attachment(self, filename: str, alias: Optional[str] = None, contenttype: Optional[str] = None, content=None):
        self.__attach.append({
            'alias': alias if isinstance(alias, str) else None,
            'filename': str(filename),
            'content': content,
            'type': contenttype if isinstance(contenttype, str) else 'application/octet-stream'
        })

    def send(self,
             host: Optional[str] = None,
             port: Optional[int] = None,
             username: Optional[str] = None,
             password: Optional[str] = None) -> bool:

        self.__errormsg = None
        msg = EmailMessage()
        recipients = list()

        for key, val in self.__headers_raw.items():
            msg[key] = val

        for key, val in self.__headers.items():
            msg[f"X-{key}"] = val

        if self.__replyto:
            msg['Reply-To'] = self.__replyto

        if self.__sender:
            msg['From'] = self.__sender

        if self.__subject:
            msg['Subject'] = self.__subject

        if len(self.__to) > 0:
            msg['To'] = tuple(self.__to)
            recipients += self.__to

        if len(self.__cc) > 0:
            msg['Cc'] = tuple(self.__cc)
            recipients += self.__cc

        if len(self.__bcc) > 0:
            msg['Bcc'] = tuple(self.__bcc)
            recipients += self.__bcc

        if self.__text:
            msg.set_content(self.__text)

        if self.__html:
            msg.add_alternative(self.__html, subtype='html')

        try:
            for attach in self.__attach:
                data = attach['content']
                maintype, subtype = attach['type'].split('/', 1)
                msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=attach['filename'])
        except Exception as e:
            logger.exception("adding attachment")
            self.__errormsg = f"failed adding attachment: {str(e.args)}"

        if host is None:
            host = self.__host

        if port is None:
            port = self.__port

        if username is None:
            username = self.__username

        if password is None:
            password = self.__password

        try:
            if port in [587, 2587]:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                with smtplib.SMTP(host, port) as s:
                    s.ehlo()
                    s.starttls(context=context)
                    s.ehlo()
                    if username:
                        s.login(username, password)
                    s.send_message(msg)
            else:
                with smtplib.SMTP(host, port) as s:
                    if username:
                        s.login(username, password)
                    s.send_message(msg)
            return True
        except Exception as e:
            msg = "tussik.email.send({}:{})".format(str(host), str(port))
            logger.exception(msg)
            self.__errormsg = f"failed sending email: {str(e.args)}"
            return False
