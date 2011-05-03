#!/bin/sh 

echo 'sort id_db'
`sort -u id_db -o tmp`
`mv tmp id_db`

echo 'sort id_fetched'
`sort -u id_fetched -o tmp`
`mv tmp id_fetched`

echo 'make new id_need_fetch'
`../tools/file-sub/file-sub id_db id_fetched > id_need_fetch`

echo 'start fetcher'
`./client_fetch_id.rb`
