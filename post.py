#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import json

headers = {"Content-Type": "application/ld+json"}

def test_sweet_post():
    data = {
        "@context": [
            "http://www.w3.org/ns/anno.jsonld",
            {
                "title": "http://thestore.swtr.in/sweets/0.1/title",
                "editable": "http://thestore.swtr.in/sweets/0.1/editable"
            }
        ],
        "type": "Annotation",
        "creator": {
            "id": "http://thestore.swtr.in/users/rkv.221",
            "type": "Person",
            "name": "RKV",
            "nickname": "rkv.221"
        },
        "body": [
            "https://en.wikipedia.org/wiki/Mysore_Palace",
            {
                "type": "TextualBody",
                "value": "Mysore Palace located at Mysore"
            },
            {
                "type": "TextualBody",
                "purpose": "tagging",
                "value": "Mysore Palace"
            },
            {
                "type": "TextualBody",
                "purpose": "tagging",
                "value": "Karnataka"
            }
        ],
        "target": {
		"source": "http://protourismindia.com/images/india-holidays-img.jpg",
		"type": "SpecificResource",
		"selector": {
			"type": "FragmentSelector",
			"conformsTo": "http://www.w3.org/TR/media-frags/",
			"value": "xywh=percent:0.009442870632672332,0.4528301886792453,0.26723323890462697,0.5283018867924528"
		},
		"renderedVia": {
			"id": "http://dash.swtr.us/#play?url=http%3A%2F%2Fprotourismindia.com%2Fimages%2Findia-holidays-img.jpg"
		}
	},
	"title": "Mysore Palace",
	"editable": "False"
	}

    resp = requests.post("http://localhost:8080/sweets/", json=data, headers=headers)
    print(resp)
    if resp.status_code != 201:
        print("its not 201 int")
    print(resp.status_code)
    print(resp.json())

def test_simple_post():
    data = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "type": "Annotation",
        "body": {
            "type": "TextualBody",
            "value": "I like this page!"
        },
        "target": "http://thestore.swtr.in/sweets/6653"
        }
    
    resp = requests.post("http://localhost:8080/tks/", json=data, headers=headers)
    print(resp)
    print(type(resp.status_code))
    print(resp.status_code)
    print(resp.json())

if __name__ == '__main__':
    #test_simple_post()
    test_sweet_post()
