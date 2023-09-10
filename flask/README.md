# Movielust API !

> API for movielust

## Local development setup

### - Requirements

| Requirement | Version | Source                                                                               |
| ----------- | ------- | ------------------------------------------------------------------------------------ |
| Python      | >3.10   | [Download link](https://www.python.org/downloads/)                                   |
| Pipenv      | latest  | `pip install Pipenv`                                                                 |
| MongoDB     | >5.0    | [Download MongoDB Community Edition](https://www.mongodb.com/try/download/community) |

### - Install Dependencies

- `git clone https://github.com/meAnurag/movielust-api.git`
- Install `Pipenv` with `pip install pipenv`
- `cd movielust-api`
- `pipenv install` - Install all dependencies
- `precommit install` - Install git hooks
- If you do not have MongoDB already installed download and install it from given link. (Install as Service to avoid starting MongoDB manually everytime.)

### - Configure Environment Variables

- Rename '_.env.example_' file to '_.env_'
- Provide values for all variables.
- | Variable      | Value                                                  |
  | ------------- | ------------------------------------------------------ |
  | FLASK_DEBUG   | development                                            |
  | SECRET        | A string to encode JWT token                           |
  | TMDB_KEY      | TMDB api key                                           |
  | MAIL_SERVER   | smtp.gmail.com                                         |
  | MAIL_EMAIL    | Your gmail address (We suggest using a dummy account.) |
  | MAIL_PASSWORD | your gmail password                                    |
  | MAIL_PORT     | 465                                                    |
  | MAIL_USE_SSL  | True                                                   |
  | MAIL_USE_TLS  | False                                                  |
  | DATABASE_URL  | mongodb://localhost:27017/                             |

### - Starting Server on localhost

- `cd movielust-api`
- `pipenv shell` - Activates virtual environment
- `py run.py` - Start server on localhost

### - Pushing changes

> '**_main_** ' and '**_development_**' branches are locked.

    Pushing directly to one of the branches will throw error.

**Steps to push**

- Create a new branch `git branch branch-name`
- Checkout to newly create branch `git checkout branch-name`
- Write your code.
- Stage files to git `git add .`
- Commit changes `git commit -m "commimt message here"`
- Push changes `git push -u origin branch-name`
- `git push` will return a url to create pull request.
- Create pull request and wait for it to be merged.
