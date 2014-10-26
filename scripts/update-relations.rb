#!/usr/bin/env ruby

require 'yaml'

m = YAML.load_file('metadata.yaml')
charm_requirements = m['requires']

relations = charm_requirements.keys.flat_map do |r| 
	[ "#{r}-relation-joined",
	  "#{r}-relation-changed", 
	  "#{r}-relation-broken"]
end + ['install', 'start', 'stop']

relations.each do |rel, value|
  `ln hooks/hooks.py hooks/#{rel}`
  `chmod +x hooks/#{rel}`
end
