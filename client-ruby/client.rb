#!/usr/bin/env ruby
# encoding: UTF-8

require 'typhoeus'
require 'json'
require 'logger'

SERVER_URL = 'http://gaisq.cs.ccu.edu.tw:4567'
NUM_GET_ID = 1000

log = Logger.new(STDOUT)
log.level = Logger::DEBUG

def parse_id(url)
  return url[42..52]
end

def get_ids
  response = Typhoeus::Request.get("#{SERVER_URL}/youtube/ids/?limit=#{NUM_GET_ID}")
  return JSON.parse(response.body)
end

def post_ids_fetched(ids)
  Typhoeus::Request.post("#{SERVER_URL}/youtube/fetched_ids/", :params => {:ids => ids.to_json})
end

def post_entry(entrys)
  Typhoeus::Request.post("#{SERVER_URL}/youtube/entrys/", :params => {:entrys => entrys.to_json})
end

log.info("client start")
queue = []
while true do
  queue += get_ids
  log.info("fetch id")

  hydra = Typhoeus::Hydra.new(:max_concurrency => 10)
  reqs = []
  queue.each do |id|
    req = Typhoeus::Request.new("http://gdata.youtube.com/feeds/api/videos/#{id}?alt=json")
    hydra.queue req
    reqs << req
  end

  hydra.run

  ids_fetched = queue
  queue = []
  entrys = []

  ban = false
  reqs.each do |req|
    res = req.response
    if res.code == 200
      entrys << JSON.parse(res.body)
    elsif res.code == 403 and res.body.index("too_many_recent_calls")
      #retry this urls next time
      id = parse_id(res.effective_url)
      queue << id
      ids_fetched.delete id
      ban = true
    end
  end

  post_entry entrys
  post_ids_fetched ids_fetched
  log.info("post entrys, size = #{entrys.size}")


  if ban
    log.info("sleep......")
    sleep(300)
  end
end
