# frozen_string_literal: true

# Class corresponding to the `url` stanza.
#
# @api private
class URL
  ATTRIBUTES = [
    :using,
    :tag, :branch, :revisions, :revision,
    :trust_cert, :cookies, :referer, :user_agent,
    :data
  ].freeze
  private_constant :ATTRIBUTES

  attr_reader :uri, :specs, *ATTRIBUTES

  extend Forwardable
  def_delegators :uri, :path, :scheme, :to_s

  def initialize(uri, **options)
    @uri        = URI(uri)
    @user_agent = :default

    ATTRIBUTES.each do |attribute|
      next unless options.key?(attribute)

      instance_variable_set("@#{attribute}", options[attribute])
    end

    @specs = options
  end
end
