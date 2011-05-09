#!/usr/bin/env ruby

require 'net/ssh'

HOSTS_CSIE = [
  {'host' => 'csie0.cs.ccu.edu.tw', 'user' => 'hcha96u', 'key' => 'AI39si6NIOXK4ebCQK62pUWZ51NMbLVuqZs0Zzg7EaAWdklU2BdOxhTF7e4Ouy41NCJVKF6b0OLDoAw6gesFbP_ptyIrjUw5aA'},
  {'host' => 'csie1.cs.ccu.edu.tw', 'user' => 'hcha96u', 'key' => 'AI39si5GEPpt-xq-hofzKAIKHPPegm-9QKl9UzJUo5_HLXnXlqN4Scow-BXMBcwpT3D0Il4XpBw42qodv1M3CUSmItvtHdc-9A'},
  {'host' => 'linux.cs.ccu.edu.tw', 'user' => 'hcha96u', 'key' => 'AI39si4awRxhrGTEQgT2KLlglIX4TdKx8vgOn9NvW4jbNPBQEyHyk4fiCXndnsrgF37QRYAKwZSdGrWy8faVWmgaSq8BG2OMjQ'},
  {'host' => 'mcore8.cs.ccu.edu.tw', 'user' => 'hcha96u', 'key' => 'AI39si5edvfQ9FZJ6KdXgkNcH4NEtZa78RonHUIRb5utt2y4k-PQGwbG6u-su42Z906DBttRThbCO9FOgt-TUluPMVsPkBPApQ'},
]

HOSTS_GAIS = [
  {'host' => '140.123.244.189', 'user' => 'nickhsu', 'key' => 'AI39si5VmAIBbBkWrA1buOpz7cPuDmdRNH6200H_mPFaADWLp9_B_fT3G-Gs9wGM2NFJIL3xu8l2HRcS86_ZFLScBr6z2WgYqA'},
  {'host' => '140.123.244.190', 'user' => 'nickhsu', 'key' => 'AI39si487bWL4Tl77mFXjw97PfHyOaE1tmNA0IYkhuCuBelvDt7ykO0lwz9X3abSFF9HSwQDDhB_tgFZYoMWmQJ85APDEL5B3Q'},
  {'host' => 'ookon.com.tw', 'user' => 'nickhsu', 'key' => 'AI39si487bWL4Tl77mFXjw97PfHyOaE1tmNA0IYkhuCuBelvDt7ykO0lwz9X3abSFF9HSwQDDhB_tgFZYoMWmQJ85APDEL5B3Q'},
]

#puts "update code in CCU CSIE"
#Net::SSH.start(HOSTS_CSIE.first['host'], HOSTS_CSIE.first['user']) do |ssh|
#  puts ssh.exec!("cd ./youtube-crawler; git pull;");
#end

HOSTS_CSIE.each do |h|
  Net::SSH.start(h['host'], h['user']) do |ssh|
    puts 'kill client in ' + h['host']
    ssh.exec!('kill `ps -l | grep python | head -n 1 | awk \'{print $2}\'`')
    puts 'start client in ' + h['host']
    ssh.exec("nohup ~/youtube-crawler/client/client.py -s gaisq.cs.ccu.edu.tw:4567 -t 10 -n 500 -k \"#{h['key']}\" > ./log#{h['host']} &")
  end
end

HOSTS_GAIS.each do |h|
  Net::SSH.start(h['host'], h['user']) do |ssh|
    puts 'kill client in ' + h['host']
    ssh.exec!('kill `ps -l | grep python | head -n 1 | awk \'{print $2}\'`')
    puts 'start client in ' + h['host']
    ssh.exec("nohup ~/tools/bin/python3 ~/youtube-crawler/client/client.py -s gaisq.cs.ccu.edu.tw:4567 -t 10 -n 500 -k \"#{h['key']}\" > ./log#{h['host']} &")
  end
end
