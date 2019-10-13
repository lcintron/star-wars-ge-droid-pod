class JSend
{
    static statusTypes = {
        ERROR:'error',
        SUCCESS:'success',
        FAIL:'fail'
    }
    
    static returnSuccess(data){
        if(!data)
            throw "Data is required on Success";
        
        let returnObj = {status:JSend.status.SUCCESS};
        returnObj.data = data;        
        return returnObj;        
    }

    static returnFail(data){
        if(!data)
            throw "Data is required on Fail";
        
        let returnObj = {status:JSend.status.FAIL};
        returnObj.data = data;
        return returnObj;        
    }

    static returnError(message, data){
        if(!message)
            throw "Message is required on Error";
        
        let returnObj = {status:JSend.status.ERROR};
        returnObj.message = message;
        if(data)
            returnObj.data = data;
        
        return returnObj;        
    }

}

module.exports = JSend;