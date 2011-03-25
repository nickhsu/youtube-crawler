#!/usr/bin/env ruby

STDIN.each_line do |line|
  line.chomp!
  puts line unless line.empty?
end
