# ZendeskZabbix-integration
Integração para criação de chamados no zendesk e atualização do chamado no zabbix

# Instalação

## No servidor
- Baixe os dois scripts (zendesk.py e zendeskEvok.sh)
- Salve eles nas pasta de scripts zabbix por padrão '/usr/local/share/zabbix/alertscripts'

## No zendesk
- Logue na ferramenta com usuário administrador
- Acesse as opções de admin
- Em canais acesse a função API
- Em configurações clique em Adicionar token da API
- De uma descrição e salve o token em algum lugar
3cm4qW73E3DotVvYuyweprEduMHttoyHm4sVSF1I
709e580cb7206c2692a5dcaac7d0f0279ee440474b77ccaf250dbc04b22ad1ca
http://172.16.224.130/api_jsonrpc.php

## No frontend
- Acesse 'Administration -> Media types' e importe o arquivo 'zendesk_python.json'
- Feito isso clique no media type importado com nome 'Zendesk Python'
- Substitua a variável <URL_ZABBIX> por 'http://<seu.ip.do.zabbix>/api_jsonrpc.php' e de um update
- Crie um usuário para envio dos tickets em 'administration -> Users -> Create User'
- Em media adicione o Zendesk Python
- No campo 'Send to' coloque o email e o token do usuário do zendesk no seguinte formato '<seu_email@seudominio.com>/token:<seu_token_zendesk>'
- Acesse 'Administration -> General -> API tokens' e crie uma nova permitindo ao usuário criado anteriormente, salve o token em algum lugar
- Entre novamente em 'Administration -> Media types -> Zendesk Python' e substitua a variável <TOKEN_ZABBIX> pelo token gerado anteriormente
- Acesse message templates e edite o subject para o endereço do seu zendesk <https://seudominio.zendesk.com>
- Salve todas as alterações
- Acesse 'Configuration -> actions -> Trigger actions' e crie uma nova action
- De um nome e em condições adicione as condições que deseja para que seja enviado um chamado para o zendesk por exemplo: 'trigger severity for maior ou igual a high', sendo assim será aberto chamado apenas para triggers high e disaster
- Em operations adicione uma Operation, defina as regras de negócio e adicione o usuário criado e send only to 'zendesk python', salve todas as alterações
