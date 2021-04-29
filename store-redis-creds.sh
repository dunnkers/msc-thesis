creds=$(heroku redis:credentials --app fseval | tail -n1)
echo $creds