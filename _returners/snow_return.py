import json
import logging
import requests
import base64
import salt.returners
import salt.utils.jid
from salt.utils.versions import LooseVersion as _LooseVersion

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = "snow"

def __virtual__():
    return __virtualname__

def _get_options(ret=None):
    """
    Get the servicenow connection options from salt.
    """
    attrs = {
        "snuri": "snuri",
        "snuser": "snuser",
        "snpass": "snpass",
    }

    _options = salt.returners.get_returner_options(
        __virtualname__, ret, attrs, __salt__=__salt__, __opts__=__opts__
    )
    return _options

def get_snow_auth_header():
    #_options = _get_options(ret)
    #snuser = _options.get("snuser")
    #snpass = _options.get("snpass")
    userpass = "saltapi:kUa=Dur0"
    encoded_u = base64.b64encode(userpass.encode()).decode()
    headers = {"Authorization" : "Basic %s" % encoded_u, "Accept": "application/json"}
    return headers

def get_snow_record(id):
    headers = get_snow_auth_header()
    #url = "https://thrivedev.service-now.com/api/now/table/u_external_event_stage?sysparm_query=u_event_external_id%3D"+id
    url = "https://thrivedev.service-now.com/api/now/table/u_thrive_monitoring_job_returns?sysparm_query=u_jid%3D"+id
    response = requests.request("GET", url, headers=headers)
    resultJson = response.json()
    record = resultJson['result'][0]
    return record

def get_snow_fun_records(fun):
    headers = get_snow_auth_header()
    url = "https://thrivedev.service-now.com/api/now/table/u_thrive_monitoring_job_returns?sysparm_query=u_function%3D"+fun
    response = requests.request("GET", url, headers=headers)
    resultJson = response.json()
    records = resultJson['result']
    return records

def create_snow_record(data, event_type):
    minion_id = data.get("minion")
    jid = data.get("jid")
    fun = data.get("fun")
    headers = get_snow_auth_header()
    # url = "https://thrivedev.service-now.com/api/now/table/u_external_event_stage"
    # payload = json.dumps({
    #     "u_config_external_id": minion_id,
    #     "u_account_external_id": minion_id,
    #     "u_source": "ThriveRMM",
    #     "u_event_type": event_type,
    #     "u_title": fun,
    #     "u_details": json.dumps(data),
    #     "u_event_external_id": jid,
    # })
    url = ""
    if(event_type == "SALT_RETURN"):
        url = "https://thrivedev.service-now.com/api/now/table/u_thrive_monitoring_job_returns"
        payload = json.dumps({
            "u_minion": minion_id,
            "u_jid": jid,
            "u_function": fun,
            "u_return_data": json.dumps(data)
        })
        requests.request("POST", url, headers=headers, data=payload)
    else:
        url = "https://thrivedev.service-now.com/api/now/table/u_thrive_monitoring_jobs"
        payload = json.dumps({
            "u_jid": jid,
            "u_function": fun,
            "u_return_data": json.dumps(data)
        })
        requests.request("POST", url, headers=headers, data=payload)  
    
def _remove_dots(src):
    """
    Remove the dots from the given data structure
    """
    output = {}
    for key, val in src.items():
        if isinstance(val, dict):
            val = _remove_dots(val)
        output[key.replace(".", "-")] = val
    return output

def returner(ret):
    """
    Return data to a mongodb server
    """
    if isinstance(ret["return"], dict):
        back = _remove_dots(ret["return"])
    else:
        back = ret["return"]

    if isinstance(ret, dict):
        full_ret = _remove_dots(ret)
    else:
        full_ret = ret
    sdata = {
            "minion": ret["id"],
            "jid": ret["jid"],
            "return": back,
            "fun": ret["fun"],
            "full_ret": full_ret,
        }
    if "out" in ret:
        sdata["out"] = ret["out"]
    create_snow_record(sdata, "SALT_RETURN")

def save_load(jid, load, minions=None):
    """
    Save the load for a given job id
    """
    create_snow_record(load, "SALT_JOB")
    #to_save = _safe_copy(load)
    # Go to SNOW Jobs Table
    #if PYMONGO_VERSION > _LooseVersion("2.3"):
        # using .copy() to ensure original data for load is unchanged
    #    mdb.jobs.insert_one(to_save)
    #else:
    #    mdb.jobs.insert(to_save)

def save_minions(jid, minions, syndic_id=None):  # pylint: disable=unused-argument
    """
    Included for API consistency
    """    

def get_load(jid):
    """
    Return the load associated with a given job id from SNOW
    """
    #conn, mdb = _get_conn(ret=None)
    #return mdb.jobs.find_one({"jid": jid}, {"_id": 0})
    snowRecord = get_snow_record(jid)
    details = json.loads(snowRecord['u_return_data'])
    return details
    
def get_jid(jid):
    """
    Return the return information associated with a jid
    """
    ret = {}
    rdata = get_snow_record(jid)
    details = json.loads(rdata['u_return_data'])
    minionId = rdata['u_minion']
    full_return = details['full_ret']
    if rdata:
            minion = minionId
            # return data in the format {<minion>: { <unformatted full return data>}}
            ret[minion] = full_return
    return ret

def get_fun(fun):
    """
    Return the most recent jobs that have executed the named function
    """
    #conn, mdb = _get_conn(ret=None)
    ret = {}
    rdata = get_snow_fun_records(fun)
    parsed = json.loads(rdata)
    ret = rdata
    return ret

def get_minions():
    """
    Return a list of minions
    """
    headers = get_snow_auth_header()
    url = "https://thrivedev.service-now.com/api/now/table/u_thrive_monitoring_job_returns?sysparm_query=u_minionISNOTEMPTY"
    response = requests.request("GET", url, headers=headers)
    resultJson = response.json()
    records = resultJson['result']
    minionArray = []
    for record in records:
        minionArray.append(record['u_minion'])

    return set(minionArray)

def get_jids():
    """
    Return a list of job ids
    """
    #conn, mdb = _get_conn(ret=None)
    # map = "function() { emit(this.jid, this); }"
    # reduce = "function (key, values) { return values[0]; }"
    # result = mdb.jobs.inline_map_reduce(map, reduce)
    # ret = {}
    # for r in result:
    #     jid = r["_id"]
    #     ret[jid] = salt.utils.jid.format_jid_instance(jid, r["value"])
    headers = get_snow_auth_header()
    url = "https://thrivedev.service-now.com/api/now/table/u_thrive_monitoring_job_returns?sysparm_query=u_minionISNOTEMPTY"
    response = requests.request("GET", url, headers=headers)
    resultJson = response.json()
    records = resultJson['result']
    ret = {}
    for record in records:
        jid = record['u_jid']
        ret[jid] = salt.utils.jid.format_jid_instance(jid, record)
    return ret
    

def prep_jid(nocache=False, passed_jid=None):  # pylint: disable=unused-argument
    """
    Do any work necessary to prepare a JID, including sending a custom id
    """
    return passed_jid if passed_jid is not None else salt.utils.jid.gen_jid(__opts__)