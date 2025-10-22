# config.py
from itsdangerous import URLSafeSerializer

SECRET_KEY = "aegjkhjaeuighaeuighauig%eua328fea"
serializer = URLSafeSerializer(SECRET_KEY)