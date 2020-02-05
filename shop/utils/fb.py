
import requests
import json
import ast
import urllib


app_id = '489170518660632'  # Replace this with your app ID
app_secret = 'EAAG85eLZC1hgBAIKVSNIRfJCtOPZBRm2qgk7ebByjXtQcFRs7Y6SrFOlne6neQAJXnP9NlLZB5MUQ2GeJH1ISnEUX8xfqH1ulFqWnf29QZBkpdHItvzqP7Gnj5p3AZAJFdZBxMxVzkGHCN7DZAnUDIGuTqpYIkZBjPuFApqh6erjpRaxW8oo3gBdQNcTXLtZAYIIs8jGrXBZAeCDZAbMzc3wjur9LD4TuzESrAqMgehe47jg8ZCnZBXrUmp8QhjqQwAv48FwZD'  # Replace this with your app secret
type_ = '192.168.43.142'
text = 'proxy'

query_params = urllib.parse.urlencode({
    'access_token': app_id + '|' + app_secret,
    'type': type_,
    'text': text
})

r = requests.get(
    'https://graph.facebook.com/v2.4/threat_indicators?' + query_params)

print(json.dumps(ast.literal_eval(r.text),
                 sort_keys=True, indent=4, separators=(',', ': ')))
