#!/usr/bin/env ruby

require 'sinatra'
require 'thin_parser'
require 'yajl/json_gem'

#const
DEFAULT_GET_LIMIT = 10000

set :environment, :production

id_db = File.open('./id_db', "a+")
id_need_fetch = File.open('./id_need_fetch', "r")
id_fetched = File.open('./id_fetched', 'a+')

#related_id_need_fetch = File.open('./related_id_need_fetch', "r")
#related_id_fetched = File.open('./related_id_fetched', "a+")

entry_new = File.open('./entry_new', 'a+')

=begin
#related id
get '/youtube/related_ids/' do
  	limit = params['limit'].nil? ? DEFAULT_GET_LIMIT : params['limit'].to_i
	ids = []
	(1..limit).each do
		begin
			line = related_id_need_fetch.readline
			line.chomp!
			ids << line
		rescue EOFError
			break
		end
	end
	ids.to_json
end

post '/youtube/related_ids/' do
	ids = JSON.parse(params['ids'])
	ids.each do |id|
		related_id_fetched.puts id
	end

end
=end

#youtube id
get '/youtube/ids/' do
	limit = params['limit'].nil? ? DEFAULT_GET_LIMIT : params['limit'].to_i
	ids = []
	(1..limit).each do
		begin
			line = id_need_fetch.readline
			line.chomp!
			ids << line
		rescue EOFError
			break
		end
	end
	ids.to_json
end

=begin
post '/youtube/ids/' do
	ids = JSON.parse(params['ids'])
    ids.each do |id|
      id_db.puts id
	end
end
=end

#youtube fetched id
post '/youtube/fetched_ids/' do
	#batch post
	fetched_ids = JSON.parse(params['ids'])
	fetched_ids.each do |id|
		id_fetched.puts id
	end
end

#youtube entry
post '/youtube/entrys/' do
	#batch post
	entrys = JSON.parse(params['entrys'])
	entrys.each do |entry|
		entry_new.puts entry
	end
end
