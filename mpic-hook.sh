#!/usr/bin/env bash
# Params passed by step-ca: token, keyAuth, domain
TOKEN="$1"
KEYAUTH="$2"
DOMAIN="$3"

API="http://coordinator/validate/http-acme"
HEADER="x-api-key: ${API_KEY}"

RESPONSE=$(curl -s -H "$HEADER" -X POST "$API" \
  -d "{\"domain\":\"$DOMAIN\",\"token\":\"$TOKEN\",\"key_authorization\":\"$KEYAUTH\",\"caa_check\":true}")

jq -e '.success == true' <<<"$RESPONSE" >/dev/null
