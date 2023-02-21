# Tussik Emailer #

Easy to create or generate an email, then send it.

1. Emailer
2. Email Builder
3. [Templating Format](docs/index.md)

## Emailer

Use an instance of the class, setting all the common parts of any email message.

```python
from tussik.email import Emailer

msg = Emailer(host="1.1.1.1")
msg.subject = "Subject"
msg.sender("user@domain.tld", "sender")
msg.to("recipient@domain.tld", "recipient")
msg.html = "<body><h1>Title</h1></body>"
msg.send()
```

## Email Builder

Email template system for building safe HTML emails. Email clients are based on an old version of HTML
with various restrictions and cosmetic anomalies.

```python
from tussik.email.Builder import EmailBuilder, EmailTemplateFormatEnum

builder = EmailBuilder()
script = "{}"
builder.load(script, EmailTemplateFormatEnum.json)

saveas_dict = builder.export()
saveas_yaml = builder.export(EmailTemplateFormatEnum.yaml)
saveas_json = builder.export(EmailTemplateFormatEnum.json)
preview = builder.preview()
saveas_html = builder.render()
```

### Load or Export

Loads a template or saves in a format of your selection

1. Dictionary
2. Yaml
3. Json

#### Editor Preview

Exports in a format that includes configuration values but
embedded with the HTML to start, exit, and body of each
render part of the template. The purpose is to help
the editor manage a presentation and configuration in one.

#### Generate Html

Accepts custom dictionaries and lists of content to be processed
with the currently loaded template.

#### Update

Working with an Emailer instance the builder will
render the subject value, html body, and smtp headers.

```python
from tussik.email.Builder import EmailBuilder, EmailTemplateFormatEnum
from tussik.email import Emailer

builder = EmailBuilder()
script = "{}"
builder.load(script, EmailTemplateFormatEnum.json)

msg = Emailer(host="1.1.1.1")
msg.sender("user@domain.tld", "sender")
msg.to("recipient@domain.tld", "recipient")
builder.update(msg)
msg.send()
```

