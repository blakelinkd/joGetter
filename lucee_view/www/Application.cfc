component displayname="Application" output="false" hint="Handle the application" {
   this.datasources["lucee"] = {
        class: 'org.postgresql.Driver'
        , bundleName: 'org.postgresql.jdbc'
        , bundleVersion: '42.2.20'
        , connectionString: 'jdbc:postgresql://db:5432/lucee'
        , username: 'lucee'
        , password: "encrypted:68566ce268ba14cc667b5f936ac883d6e959ab7c9d679cbf"
        
        // optional settings
        , connectionLimit:100 // default:-1
        , liveTimeout:15 // default: -1; unit: minutes
        , validate:false // default: false
    };

    
    component {
    this.name = "YourApplicationName";
    // Initialize your REST application
    restInitApplication(
        directoryPath="controllers",
        serviceMapping="hello"
    );
}
    /**
    * @hint First function run when Lucee receives the first request. 
    */
    public boolean function OnApplicationStart(){
        return true;
    }
    /**
    * @hint onApplicationEnd() is triggered when the application context ends, means when the 
    * timeout of the application context is reached (this.applicationTimeout). 
    */
    public void function onApplicationEnd( struct application ){
        return;
    }
    /**
    * @hint onSessionStart() is triggered with every request that has no session 
    * defined in the current application context. 
    */
    public void function onSessionStart(){
        return;
    }
    /**
    * @hint onSessionEnd() is triggered when a specific session context ends, 
    * when the timeout of a session context is reached (this.sessionTimeout). 
    */
    public void function onSessionEnd( struct session, struct application ){
        return;
    }
    /**
    * @hint onRequestStart() is triggered before every request, so you can 
    * prepare the environment for the request, for example to produce the HTML 
    * header or load some data/objects used within the request. 
    */
    public boolean function onRequestStart( string targetPage ){
        return true;
    }
    /**
    * @hint onRequest() is triggered during a request right after onRequestStart() ends and before 
    * onRequestEnd() starts. Unlike other CFML engines, Lucee executes this function without looking 
    * for the "targetPage" defined, while other CFML engines will complain if the targetPage doesn't 
    * physically exist (even if not used in the onRequest() function) 
    */
    public void function onRequest( string targetPage ){
        include arguments.targetPage;
        return;
    }
    /**
    * @hint onRequest() is triggered at the end of a request, right after onRequest() finishes. 
    */
    public void function onRequestEnd(){
        return;
    }
    /**
    * @hint onCFCRequest() is triggered during a request for a .cfc component, typically
    * used to handle remote component calls (e.g. HTTP Webservices). 
    */
    public void function onCFCRequest( string cfcName, string methodName, struct args ){
        return;
    }
    /**
    * @hint onError() is triggered when an uncaught exception occurs in this application context. 
    */
    public void function onError( struct exception, string eventname ){
        return;
    }
    /**
    * @hint OnAbort() is triggered when a request is ended with help of the "abort" tag. 
    */
    public void function  onAbort( string targetPage ){
        return;
    }
    /**
    * @hint onDebug() is triggered when debugging is enabled for this request.
    */
    public void function onDebug( struct debuggingData ){
        return;
    }
    /**
    * @hint onMissingTemplate() is triggered when the requested page wasn't found and no "onRequest()" 
    * function is defined.
    */
    public void function onMissingTemplate( string targetPage ){
        return;
    }
}


