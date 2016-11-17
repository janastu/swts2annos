#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import json

headers = {"Content-Type": "application/ld+json"}

def get_renos():
    pass

def get_annos(anno_type):
    resp = requests.get("http://thestore.swtr.in/api/sweets/q?what={}".format(anno_type))

    for anno in resp.json():
        data = {
            "@context": [
                "http://www.w3.org/ns/anno.jsonld",
                {
                    "title": "http://thestore.swtr.in/sweets/0.1/title",
                    "editable": "http://thestore.swtr.in/sweets/0.1/editable"
                }
            ],
            "type": "Annotation",
        }
        data["id"] = "http://thestore.swtr.in/sweets/{}".format(anno["id"])
        data["creator"] = {
            "id": "http://thestore.swtr.in/users/{}".format(anno["user_id"]),
            "type": "Person",
            "name": anno["who"]
        }
        if 'title' in anno['how']:
            data['title'] = anno['how']['title']
        if 'editable' in anno['how']:
            data['editable'] = anno['how']['editable']

        data["body"] = []
        if 'link' in anno['how']:
            data['body'].append(anno['how']['link'])
        if 'tags' in anno['how']:
            for tag in anno['how']['tags']:
                data['body'].append({
                    "type": "TextualBody",
                    "purpose": "tagging",
                    "value": tag
                })
        if 'comment' in anno['how']:
            data['body'].append({
                "type": "TextualBody",
                "value": anno['how']['comment']
            })


        data['target'] = {}
        data['target']['source'] = anno['where']
        data['target']['type'] = "SpecificResource"
        if len(anno['how']['shapes']) == 1:
            data['target']['selector'] = {}
            data['target']['selector']['type'] = "FragmentSelector"
            data['target']['selector']['conformsTo'] = "http://www.w3.org/TR/media-frags/"
            data['target']['selector']['value'] = "xywh=percent:{x},{y},{width},{height}".format(**anno['how']['shapes'][0]['geometry'])
        else:
            data['target']['selector'] = []
            for shape in anno['how']['shapes']:
                geom = shape['geometry']
                data['target']['selector'].append({
                    "type": "FragmentSelector",
                    "conformsTo": "http://www.w3.org/TR/media-frags/",
                    "value": "xywh=percent:{x},{y},{width},{height}".format(**shape['geometry'])
                })

        if 'origin' in anno['how']:
            data['target']['renderedVia'] = {
                    "id": anno['how']['origin']
            }

        resp = requests.post("http://localhost:8080/sweets/", json=data, headers=headers)

        if resp.status_code != 201:
            print("Error uploading sweet")
            print(resp.json())

if __name__ == "__main__":
    import sys
    get_annos(sys.argv[1])
