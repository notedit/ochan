

import requests

for i in range(0,100):
    req = requests.post('http://localhost:8000/publish/test',
                json={'test':'test'}
            )
    print(req.text)

