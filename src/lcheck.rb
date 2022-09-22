require 'asciidoctor'
require 'faraday'
require 'thread'


@expanded_files = []

for arg in ARGV
    array = arg.split(',')
    for i in array
        i.delete! '[]'
        unless @expanded_files.include?(i)
            @expanded_files << i
        end
    end
end


def return_broken_links()
    #Parses the file for links; excludes pseudo links
        #e.g. xrefs
    #Creates a hash with links as keys and file paths as values
        #e.g. hash = {'www.example.com'=>['path/to/file1.adoc', 'path/to/file2.adoc']}
    #Runs link checker and prints the results.
    files_checked = []
    links_dict = {}

    @expanded_files.each do |file|
        Asciidoctor::LoggerManager.logger.level = :fatal
        doc = Asciidoctor.convert_file file, safe: :safe, catalog_assets: true, sourcemap: true
        doc.find_by(context: :paragraph).each do |l|
            realpath = File.realpath(l.file)

            unless files_checked.include?(realpath)
                files_checked << realpath
            end

            links = l.content.scan(/(?<=href\=")[^\s]*(?=">)|(?<=href\=")[^\s]*(?=" class="bare")/)

            if not links.empty?
                links.each do |link|
                    next if link.start_with?( '#', '/', 'tab.', 'file', 'mailto', 'ftp://') or link.downcase.include?('example') or link.downcase.include?('tools.ietf.org') or link.empty? or link == 'ftp.gnome.org'
                    if not links_dict.key?(link)
                        links_dict[link] = [l.file]
                    else
                        if not links_dict[link].include?(l.file)
                            links_dict[link].push(l.file)
                        end
                    end
                end
            end
        end
    end

    broken_links = queue_broken_links(links_dict)

    puts "\nStatistics:"
    puts "Input files: #{@expanded_files.size}. Files checked: #{files_checked.size}. Errors found: #{broken_links}."
    exit 1

end


def print_msg(link, error_type, files)
    puts "\nLink: #{link}"
    puts "Response code: #{error_type}"

    if files.count > 1
        puts "File count: #{files.count}"
    end
    puts "File path: #{files.join(", ")}"
end


def queue_broken_links(links_dict)
    # Takes in the \nLink: path hash
        # #e.g. hash = {'www.example.com'=>['path/to/file1.adoc', 'path/to/file2.adoc']}
    # Runs link check on the hash keys
    # Returns the list of broken links (for statistics)
    # Handles exceptions
    broken_links = 0

    semaphore = Queue.new
    10.times { semaphore.push(1) }

    threads = []

    links_dict.each do |link,files|
        threads << Thread.new do
            semaphore.pop

            encoded_link = CGI.escape(link)

            conn = Faraday.new(url: encoded_link) do |faraday|
                faraday.response :raise_error
            end

            begin
                conn.get(link)
            rescue URI::BadURIError => e
                broken_links += 1
                error_type = 'Bad URI'
                print_msg(link, error_type, files)

            rescue URI::InvalidURIError => e
                broken_links += 1
                error_type = 'Invalid URL'
                print_msg(link, error_type, files)

            rescue Faraday::Error => e
                broken_links += 1
                error_type = e.response[:status]
                print_msg(link, error_type, files)

            end
            semaphore.push(1) # Release token
        end
    end

    threads.each(&:join)

    return broken_links
end

return_broken_links()
