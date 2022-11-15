"""
Django command to wait for elastic search container to start
"""

import time
import requests
from elasticsearch import Elasticsearch
from django.core.management.base import BaseCommand


def isrunning():
    try:
        res = requests.get("http://localhost:9200/_cluster/health")
        if res.status_code == 200:
            if res.json()["number_of_nodes"] > 0:
                return True
        return False
    except Exception as e:
        return e


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for Elasticsearch cluster...")
        Elasticsearch(hosts=[{"host": "elasticsearch", "port": 9200}])
        connected = False
        while not connected:
            try:
                isrunning()
                connected = True
            except Exception:
                self.stdout.write("Cluster not available yet ...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Cluster available!"))
