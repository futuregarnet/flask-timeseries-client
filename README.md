# Predix Arcade Data Client

This client serves as a basic Predix data client that can be used to query the Predix Timeseries service using Python/Flask. The repo only includes minimal classes.

The main dependency is the [PredixPy SDK](https://predixpy.run.aws-usw02-pr.ice.predix.io/index.html) which uses the Predix services variables set in config.json.

This API is meant to abstract the Timeseries API and simplify authentication and requests.


## Development Setup

If you're working through my Predix Arcade series, this data client is the 1st step in creating a full Predix Arcade app that monitors an arcade asset (NES emulator). Be sure to complete this tutorial first.

1. **[Predix Arcade Data Client](https://github.com/futuregarnet/predix-arcade-data-client#predix-arcade-data-client)**
1. [Predix Arcade](https://github.com/futuregarnet/predix-arcade#predix-arcade)
1. [Predix Arcade Dashboard Starter Kit](https://github.com/futuregarnet/predix-arcade-dashboard-starter-kit#predix-arcade-dashboard-starter-kit)

Clone or download and extract the source code:

```shell
git clone https://github.com/futuregarnet/predix-arcade-data-client.git
cd predix-arcade-data-client
```

### Package Manager Installation

If you don't have them already, Python 3 (including pip) installed:

1. Install [Python 3.6](https://www.python.org/downloads/release/python-366/):
  - Windows: Be sure to click **Add Python 3.6 to PATH** [See Docs](https://docs.python.org/3/using/windows.html#installation-steps)
  - Mac: `brew install python`

**Note**: (Windows Only) - If Python was installed but not added to PATH:
1. Re-run the installer
1. Select the **Modify** option
1. Click **Next**
1. Check the **Add Python to environment variables** option and click **Install**

### Dependency Installation

This app uses packages managed by pip. Issue the following command to install them:

```shell
pip install -r requirements.txt
```

### Local Configuration

You will need to create Predix UAA and Timeseries instances and update the config.json file with their details. To learn how to create Predix UAA Predix Timeseries instances, follow [this guide](https://www.predix.io/resources/tutorials/tutorial-details.html?tutorial_id=1544).

Edit the config.json file and add the following details:

- **<UAA_TENANT_ID>**: Predix UAA Tenant ID
- **<PREDIX_APP_CLIENT_ID>**: Predix UAA Client ID
- **<PREDIX_APP_CLIENT_SECRET>**: Predix UAA Client Secret
- **<PREDIX_DATA_TIMESERIES_ZONE_ID>**: Predix Timeseries Zone ID

**NOTE**: Because these file can contain sensitive information about your Predix services, config.json and manifest.yml should not be pushed to GitHub during commits.

## Local Development (Linux/Mac Only)

To start the app locally, issue the command:

```shell
gunicorn manage:app --log-config logging.ini [--bind localhost:<PORT>] [--reload]
```

- Optional Arguments:
  - `--bind`: By default, gunicorn runs on port 8000. Bind a different `<PORT>` if desired.
  - `--reload`: Automatically reload gunicon workers when source files are updated

To test the API, use an API tool (i.e. [Postman](https://www.getpostman.com/)) to send requests to [localhost:8000](http://localhost:8000) (change your port if different)

### API Routes

The following API routes are available for Timeseries data tasks:
                                                  
API Route | Method | Description | Body Format                                   
------------ | ------------- | ------------- | -------------                               
/api/v1/tags | GET | Get list of available tag names | N/A
/api/v1/latest | POST | Get the latest datapoint for each of requested tags | `{"tags": ["<TAG_NAME_1>", ...]}`
/api/v1/datapoints | POST | Get 10000 of the last datapoints for each of requested tags | `{"tags": ["<TAG_NAME_1>", ...]}`
/api/v1/ingest | POST | Upload datapoints into timeseries | `{"datapoints": [{"name": "<TAG_NAME_1>", "value": "<VALUE>", "attributes": {"<KEY>": "<VALUE>"}}, ...]}`

## Predix Deployment

The `manifest.yml` file is used for application configuration on the Predix platform. Edit the `manifest.yml` file with:

- **<PREDIX_UAA_SERVICE>**: Your UAA Instance Name
- **<PREDIX_TIMESERIES_SERVICE>**: Your Time Series Instance Name
- **<PREDIX_APP_CLIENT_ID>**: Your UAA Client ID
- **<PREDIX_APP_CLIENT_SECRET>**: Your UAA Client Secret


Use the following commands to push to Predix:

```shell
cf push [-n <APP_NAME>]
```

- `-n`: Provide a custom app name (also used for the URL)
  - You can also update the **name** attribute in `manifest.yml` to a custom app name and remove the **random-route** attribute to avoid this parameter.
