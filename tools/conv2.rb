#!/usr/bin/env ruby
# encoding: UTF-8

require 'yajl/json_gem'
require 'pp'

def json2gais(data)
  begin
    buf = "@\n"
    buf += "@id:#{data['entry']['id']['$t']}\n"
    #buf += "@published:#{data['entry']['published']['$t']}\n"
    #buf += "@updated:#{data['entry']['updated']['$t']}\n"
    buf += "@title:#{data['entry']['title']['$t']}\n"
    #buf += "@content:#{data['entry']['content']['$t']}\n"
    #buf += "@author:#{data['entry']['author'][0]['name']['$t']}\n"
    buf += "@keyword:#{data['entry']['media$group']['media$keywords']['$t']}\n"
    buf += "@favoriteCount:#{data['entry']['yt$statistics']['favoriteCount']}\n"
    buf += "@viewCount:#{data['entry']['yt$statistics']['viewCount']}\n"
    #buf += "@duration:#{data['entry']['media$group']['yt$duration']['seconds']}\n"
    buf += "@category:#{data['entry']['category'][1]['label']}\n"

    #get video source
    buf += "@src:"
    data['entry']['media$group']['media$content'].each do |c|
      buf += c['url'] if c['type'] == "application/x-shockwave-flash"
    end
    buf += "\n"

    #format = ''
    #data['entry']['media$group']['media$content'].each do |c|
    #  format += "#{c['yt$format']},"
    #end
    #buf += "@format:#{format}"

    return buf
  rescue
    return nil
  end
end

STDIN.each_line do |line|
  line.chomp!
  begin
    entry = JSON.parse(line)
    #puts entry.pretty_inspect
    #break
    if entry['entry']['category'][1]['label'] == 'Music'
      gais = json2gais(entry)
      puts gais unless gais.nil?
    end
  rescue
  end
  #break
end
