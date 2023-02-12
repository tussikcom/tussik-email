from tussik.email import Emailer


class TestEmailing:
    def test_basic(self) -> None:
        smtp = Emailer(host="1.1.1.1")
        smtp.subject = "Subject"
        smtp.sender("user@domain.tld", "sender")
        smtp.to("recipient@domain.tld", "recipient")
        smtp.send()
