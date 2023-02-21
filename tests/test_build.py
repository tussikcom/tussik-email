import os

from tussik.email.Builder import EmailBuilder, EmailTemplateFormatEnum

g_template = {
    "page": {
        "width": 800
    },
    "fonts": [
        {"name": "Helvetica"},
        {"name": "serif"},
        {"name": "Arial"}
    ],
    "footer": {
        "height": 200,
        "script": "My Footer Text",
        "halign": "right"
    },
    "preview": {
        "script": "message with a value of {{value}}"
    },
    "subject": {
        "script": "[TEST] Product {{productname}} is amazing"
    },
    "headers": {
        "key1": "value{number}",
        "key2": "{specialvalue}"
    },
    "sections": [
        {
            "hide": "{{ productname.startswith('XAcme') }}",
            "segments": [
                {
                    "width": "50%",
                    "renders": [
                        {
                            "type": "button",
                            "url": "https://tussik.com",
                            "text": "Tussik"
                        },
                        {
                            "type": "text",
                            "script": "Hello World"
                        }
                    ]
                }
            ]
        }
    ]
}


class TestBuilding:
    def test_basic(self) -> None:
        people = [
            {'name': 'Mike'},
            {'name': 'John'},
            {'name': 'Tom'},
            {'name': 'Craig'},
        ]

        eb = EmailBuilder()
        eb.load(g_template)
        saveas = eb.export()
        saveas_yaml = eb.export(EmailTemplateFormatEnum.yaml)
        saveas_json = eb.export(EmailTemplateFormatEnum.json)
        preview = eb.preview()
        html = eb.render(debug=True, people=people, productname="Acme Corp")
        subject = eb.subject(people=people, productname="Acme Corp")

        fn = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../basic.html"))
        with open(fn, "w+") as f:
            f.write(html)
            f.flush()
        assert True
