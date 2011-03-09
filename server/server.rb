#!/usr/bin/env ruby

require 'sinatra'
require 'thin_parser'
require 'json'
require 'zlib'

#const
DEFAULT_GET_LIMIT = 10000

id_db = File.open('./id', "a+")
fetched_id_db = File.open('./fetched_id', 'a+')
entry_db = File.open('./entry', 'a+')

#youtube id
get '/youtube/ids/' do
	limit = params['limit'].nil? ? DEFAULT_GET_LIMIT : params['limit'].to_i
	ids = []
	(1..limit).each do
		begin
			line = id_db.readline
			line.chomp!
			ids << line
		rescue EOFError
			break
		end
	end
	ids.to_json
end

post '/youtube/ids' do
	ids = JSON.parse(params['ids'])
	ids.each do |id|
		id_db.put id
	end
end

#youtube fetched id
post '/youtube/fetched_ids/' do
	#batch post
	fetched_ids = JSON.parse(params['ids'])
	fetched_ids.each do |id|
		fetched_id_db.puts id
	end
end

#youtube entry
post '/youtube/entrys/' do
	#batch post
	entrys = JSON.parse(params['entrys'])
	entrys.each do |entry|
		entry_db.puts entry
	end
end
