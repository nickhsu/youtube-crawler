#!/usr/bin/env ruby

require 'cgi'
require 'typhoeus'
require 'json'

def search_video_raw(args)
  url = "http://gdata.youtube.com/feeds/api/videos?"
  args.each_pair do |k, v|
    url += "&#{k.to_s}=#{CGI::escape(v.to_s)}"
  end

  return Typhoeus::Request.get(url).body
end

STDIN.each_line do |line|
  key = line.chomp!
  (0..9).each do |j|
    data = search_video_raw("q" => key, "max-results" => 50, "index" => j * 50 + 1, "alt" => "json")
    if data.index("too_many_recent_calls")
      sleep(120)
      redo
    end
    json = JSON.parse(data)
    break if json.nil? or json['feed']['entry'].nil?
    json['feed']['entry'].each do |e|
      puts e['id']['$t'].split('/')[-1]
    end
  end
end
