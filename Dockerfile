FROM python:3.12.3-bookworm as base
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Ruby environment is just for Kamal.
FROM ruby:3.2.2-bookworm as ruby
ENV BUNDLE_PATH="/usr/local/bundle"
COPY .ruby-version Gemfile Gemfile.lock ./
RUN bundle install
RUN rm -rf ~/.bundle "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git

# Final stage for app image with built artifacts.
FROM base
COPY --from=ruby /usr/local/bundle /usr/local/bundle
COPY . .
RUN ./manage.py collectstatic
RUN rm -rf .git

EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "gregschmit.asgi:application"]
