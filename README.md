# Alertmanager webhook for Telegram

Send alert notifications to multiple destinations.

Exp:
- service A send to user1
- service B send to user2
- service C send to user1 + user2

### Create bot notify

- chat with @BotFather

- get botToken

### Change on run.py

- botToken

### Change on user.json

- /start with @userinfobot and add chatID to user.json

### Running

```
git clone https://github.com/thangtq710/Alertmanager-webhook-telegram.git
docker build -t alertmanager-webhook-telegram:1.0 .
docker run -d --name telegram-bot -p 5000:5000 alertmanager-webhook-telegram:1.0
```

### Alerting rules config example

```
groups:
- name: kong-http-error
  rules:
  - alert: kong-http-error-serviceA
    expr: sum(rate(kong_http_status{code=~"50(2|3)", service="serviceA"}[5m])) by (service) / sum(rate(kong_http_status[5m])) by (service) * 100 > 1
    for: 10s
    labels:
      severity: warning
      group_id: kong-http-error
    annotations:
      summary: "APIGateway HTTP Error 5xx rate"
      description: "HTTP requests with status 5xx in {{ $labels.service }}: {{ $value }}%"
      
  - alert: kong-http-error-serviceB
    expr: sum(rate(kong_http_status{code=~"50(2|3)", service="serviceB"}[5m])) by (service) / sum(rate(kong_http_status[5m])) by (service) * 100 > 1
    for: 10s
    labels:
      severity: warning
      group_id: kong-http-error
    annotations:
      summary: "APIGateway HTTP Error 5xx rate"
      description: "HTTP requests with status 5xx in {{ $labels.service }}: {{ $value }}%"
  - alert: kong-http-error-serviceC
    expr: sum(rate(kong_http_status{code=~"50(2|3)", service="serviceC"}[5m])) by (service) / sum(rate(kong_http_status[5m])) by (service) * 100 > 1
    for: 10s
    labels:
      severity: warning
      group_id: kong-http-error
    annotations:
      summary: "APIGateway HTTP Error 5xx rate"
      description: "HTTP requests with status 5xx in {{ $labels.service }}: {{ $value }}%"
```

### Alertmanager config example

```
global:
  resolve_timeout: 1m
  slack_api_url: https://api.slack.com
route:
# group_by: ['alertname', 'severity']
  receiver: thangtqlabs

  routes:
  - receiver: "kong-http-error-serviceA"
    group_by:
    - group_id
    - service
    match:
      group_id: kong-http-error 
      service: serviceA
    continue: true
    group_wait: 3s
    group_interval: 3s
    repeat_interval: 60m

  - receiver: "kong-http-error-serviceB"
    group_by:
    - group_id
    - service
    match:
      group_id: kong-http-error
      service: serviceB
    continue: true
    group_wait: 3s
    group_interval: 3s
    repeat_interval: 60m

  - receiver: "kong-http-error-serviceC"
    group_by:
    - group_id
    - service
    match:
      group_id: kong-http-error
      service: serviceC
    continue: true
    group_wait: 3s
    group_interval: 3s
    repeat_interval: 60m

receivers:
- name: thangtqlabs
  slack_configs:
  - send_resolved: false
    channel: '#alert'
    title_link: ""
- name: "kong-http-error-serviceA"
  webhook_configs:
  - url: 'http://10.1.1.1:5000/notify/thangtq'
    send_resolved: false
- name: "kong-http-error-serviceB"
  webhook_configs:
  - url: 'http://10.1.1.1:5000/notify/huylv'
    send_resolved: false
- name: "kong-http-error-serviceC"
  webhook_configs:
  - url: 'http://10.1.1.1:5000/notify/thangtq'
    send_resolved: false
  - url: 'http://10.1.1.1:5000/notify/huylv'
    send_resolved: false
  - - url: 'http://10.1.1.1:5000/notify/adt-devops'
    send_resolved: true
```
