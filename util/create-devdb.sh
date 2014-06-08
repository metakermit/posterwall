db=posterwall
dbuser=posterwall

createdb $db
createuser $dbuser
psql posterwall -c "GRANT ALL PRIVILEGES ON DATABASE $db TO $dbuser;"
