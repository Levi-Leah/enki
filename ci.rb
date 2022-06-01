#!/usr/bin/env ruby

require 'find'
require 'asciidoctor'
require 'open3'

# should be replaced by the git repo root
pwd = '/home/levi/rhel-8-docs/'

# should be replaced by a changed files var
stdout, stderr, status = Open3.capture3( "git diff --diff-filter=ACM --name-only master...$(git rev-parse --abbrev-ref HEAD) -- '*.adoc'")
changed_files = stdout.split("\n")

master_adocs = []

Find.find(pwd) do |path|
  master_adocs << path if path =~ /.*\master.adoc$/
end

affected_master = []

'''master_adocs.each do |file|
    doc = Asciidoctor.load_file file, safe: :safe, catalog_assets: true
    doc.catalog[:includes].each do |inc, _|
        puts changed_files.any? incy
        #puts changed_files.any? "#{inc}.adoc"
    end
end'''


a = ["rhel-8/modules/cockpit/con_what-is-the-RHEL-web-console.adoc" "bdsjvgfdj/rhel-8/modules/cockfdpit/con_what-isgfh-the-RHEL-web-console.adoc"]

puts a.any? "rhel-8/modules/cockpit/con_what-is-the-RHEL-web-console.adoc"
