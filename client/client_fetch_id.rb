#!/usr/bin/env ruby
# encoding: UTF-8

require 'typhoeus'
require 'json'
require 'logger'

log = Logger.new(STDOUT)
log.level = Logger::DEBUG
id_db = File.open('id_db', "a+")
id_need_fetch = File.open('id_need_fetch', "r")
id_fetched = File.open('id_fetched', "a+")

def parse_id(url)
  return url[42..52]
end

def parse_related_id(data)
  related_ids = []
  json = JSON.parse(data)

  return [] unless json['feed']['entry']
  json['feed']['entry'].each do |t|
    related_ids << parse_id(t['id']['$t'])
  end

  return related_ids
end

log.info("client start")
while true
  #read unfetched id
  queue = []
  begin
    1000.times do
      id = id_need_fetch.readline.chomp!
      queue << id unless id.empty?
    end
  rescue EOFError
    break
  end

  hydra = Typhoeus::Hydra.new(:max_concurrency => 10)
  reqs = []
  header = {"Accept-Encoding" => "gzip,deflate,sdch"}

  queue.each do |id|
    req = Typhoeus::Request.new("http://gdata.youtube.com/feeds/api/videos/#{id}/related?max-results=50&fields=entry(id)&alt=json",
                                :header => header)
    hydra.queue req
    reqs << req
  end

  log.info("fetch data")
  hydra.run

  ban = false
  reqs.each do |req|
    next unless req
    res = req.response
    if res.code == 200
      parse_related_id(res.body).each do |id|
        id_db.puts id.chomp
      end
      id_fetched.puts parse_id(res.effective_url)
    elsif res.code == 403 and res.body.index("too_many_recent_calls")
      #retry this urls next time
      queue << parse_id(res.effective_url).chomp
      ban = true
    else
      #other error, e.g. video not found
      id_fetched.puts parse_id(res.effective_url).chomp
    end
  end

  if ban
    log.info("sleep")
    sleep(300)
  end

end
