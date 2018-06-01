# Flask Predix Timeseries Client

This client serves as a basic Predix data client that can be used to query the Predix Timeseries service using Python/Flask. The repo only includes minimal classes.

The main dependency is the [PredixPy SDK](https://predixpy.run.aws-usw02-pr.ice.predix.io/index.html) which uses the Predix services variables set in config.json.

This API is meant to abstract the Timeseries API and simplify authentication and requests.


## Getting Started

Make a directory for your project.  Clone or download and extract the repo in that directory.

```shell
git clone https://github.com/futuregarnet/flask-timeseries-client.git
cd flask-timeseries-client
```

### Install Tools
If you don't have them already, you'll need Python 2 installed globally on your machine.

1. Install [Python 2.7](https://www.python.org/downloads/release/python-2715/)

### Install the Dependencies
This app uses packages managed by pip. Issue the following command to install them:

```shell
pip install -r requirements.txt
```

## Configure Local Environment

You will need to create Predix UAA and Timeseries instances and update the config.json file with their details. To learn how to create Predix UAA Predix Timeseries instances, follow [this guide](https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1544).

You will need to copy the config and manifest templates to file locations that the app can locate.

```shell
cp config-template.json config.json
cp manifest-template.yml manifest.yml
```

Edit the config.py and manifest.yml files and replace the following placeholders with your Predix service information:
- **<PREDIX_SECURITY_UAA_URI>**: Predix UAA URI (US-West: https://<UAA_TENANT_ID>.predix-uaa.run.aws-usw02-pr.ice.predix.io)
- **<PREDIX_APP_CLIENT_ID>**: Predix UAA Client ID
- **<PREDIX_APP_CLIENT_SECRET>**: Predix UAA Client Secret
- **<PREDIX_DATA_TIMESERIES_ZONE_ID>**: Predix Timeseries Zone ID
- **<PREDIX_DATA_TIMESERIES_INGEST_URI>**: Predix Timeseries Ingestion URI (US-West: wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages)
- **<PREDIX_DATA_TIMESERIES_QUERY_URI>**: Predix Timeseries Query URI (US-West: https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io)

**NOTE**: Because these file contains sensitive information about your Predix services, config.py and manifest.yml have been added to the .gitignore file and will not be pushed to GitHub during commits.

## Local Development

To start the app locally, issue the command:

```shell
gunicorn manage:app --log-config logging.ini [--bind localhost:<PORT>] [--reload]
```

- Optional Arguments:
  - `--bind`: By default, gunicorn runs on port 8000. Bind a different `<PORT>` if desired.
  - `--reload`: Automatically reload gunicon workers when source files are updated

To test the API, use an API tool (i.e. [Postman](https://www.getpostman.com/)) to send requests to [localhost:8000](http://localhost:8000) (change your port if different)

### APIs                                                  
API Route | Method | Description | Body Format                                   
------------ | ------------- | ------------- | -------------                               
/api/v1/tags | GET | Get list of available tag names | N/A
/api/v1/latest | POST | Get the latest datapoint for each of requested tags | `{"tags": ["<TAG_NAME_1>", ...]}`
/api/v1/datapoints | POST | Get 10000 of the last datapoints for each of requested tags | `{"tags": ["<TAG_NAME_1>", ...]}`
/api/v1/ingest | POST | Upload datapoints into timeseries | `{"datapoints": [{"name": "<TAG_NAME_1>", "value": "<VALUE>", "attributes": {"<KEY>": "<VALUE>"}}, ...]}`

## Deployment
You will also need to update the manifest template with your app and service names. Edit the manifest.yml file and add the following details:
 - **name**:
   - **APP_NAME**: App name
 - **services**: 
   - **PREDIX_UAA_SERVICE** UAA instance name
   - **PREDIX_TIMESERIES_SERVICE** Timeseries instance name

Push the app to the cloud using:

```shell
cf push
```

Once the upload and deployment are complete, the output should look something like this:

```shell
App ???????? was started using this command `gunicorn manage:app --log-config logging.ini`

Showing health and status for app ??????? in org ??? / space ??? as ???...
OK

requested state: started
instances: 1/1
usage: 128M x 1 instances
urls: <INSERT_APP_NAME>.run.aws-usw02-pr.ice.predix.io
last uploaded: ??? ??? ## ##:##:## UTC 20##
stack: cflinuxfs2
buildpack: python_buildpack

     state     since                    cpu     memory          disk           details
#0   running   20##-##-## ##:##:## ?M   ##.#%   ##.#M of 128M   ###.#M of 1G
```

You can access your application using the URL provided.

**NOTE**: You'll have to prepend the URL with https:// (e.g. https://&lt;APP_NAME&gt;.run.aws-usw02-pr.ice.predix.io).