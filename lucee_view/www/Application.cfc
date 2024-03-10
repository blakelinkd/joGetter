component displayname="Application" output="false" hint="Handle the application" {
    /***************************************************************************
    * INTRODUCTION
    ****************************************************************************
    *  This Application.cfc template should serve as a 
    *  starting point for your applications settings running
    *  with Lucee CFML engine. 
    * 
    *  The settings/definitions are set as comments and represent Lucees default
    *  settings. Some settings/definitions should only serve as helping 
    *  examples, e.g. datasources, mailservers, cache, mappings
    *
    *  When creating an Application.cfc for the first time, you can configure 
    *  all the settings within the Lucee Server or Web Administrator 
    *  and use its "Export" tool ( Lucee Adminisitrator => Settings => Export )  
    *  to move (by copy and paste) the settings to your Application.cfc.
    * 
    *  For further reference please see the following documentation at:
    *  https://docs.lucee.org/categories/application.html
    *  https://docs.lucee.org/guides/cookbooks/application-context-basic.html
    *  https://docs.lucee.org/reference/tags/application.html
    *  https://docs.lucee.org/guides/Various/system-properties.html
    * 
    ***************************************************************************/
   ////////////////////////////////////////////////////////////////
   //  APPLICATION NAME
   //  Defines the name of your application
   ////////////////////////////////////////////////////////////////
   // this.name = "myApplication";
   ////////////////////////////////////////////////////////////////
   //  LOCALE
   //  Defines the desired time locale for the application
   ////////////////////////////////////////////////////////////////
   // this.locale = "en_US"; 
   ////////////////////////////////////////////////////////////////
   //  TIME ZONE
   //  Defines the desired time zone for the application
   ////////////////////////////////////////////////////////////////
   // this.timezone = "Europe/Berlin"; 
   ////////////////////////////////////////////////////////////////
   //  WEB CHARSET
   //  Default character set for output streams, form-, url-, and 
   //  cgi scope variables and reading/writing the header
   ////////////////////////////////////////////////////////////////
   // this.charset.web="UTF-8";
   ////////////////////////////////////////////////////////////////
   //  RESOURCE CHARSET
   //  Default character set for reading from/writing to 
   //  various resources
   ////////////////////////////////////////////////////////////////
   // this.charset.resource="windows-1252";
   ////////////////////////////////////////////////////////////////
   //  APPLICATION TIMEOUT
   //  Sets the amount of time Lucee will keep the application scope alive. 
   ////////////////////////////////////////////////////////////////
   //  this.applicationTimeout = createTimeSpan( 1, 0, 0, 0 ); 
   ////////////////////////////////////////////////////////////////
   //  SESSION TYPE
   //  Defines the session engine 
   //  - Application: Default cfml sessions
   //  - JEE: JEE Sessions allow to make sessions over a cluster. 
   ////////////////////////////////////////////////////////////////
   // this.sessionType = "application"; 
   ////////////////////////////////////////////////////////////////
   //  SESSION MANAGEMENT
   //  Enables/disables session management
   ////////////////////////////////////////////////////////////////
   // this.sessionManagement = true;
   ////////////////////////////////////////////////////////////////
   //  SESSION TIMEOUT
   //  Sets the amount of time Lucee will keep the session scope alive. 
   ////////////////////////////////////////////////////////////////
   // this.sessionTimeout = createTimeSpan( 0, 0, 30, 0 ); 
   ////////////////////////////////////////////////////////////////
   //  SESSION STORAGE
   //   Default Storage for Session, possible values are:
   //  - memory: the data are only in the memory, so in fact no persistent storage
   //  - file: the data are stored in the local filesystem
   //  - cookie: the data are stored in the users cookie
   //  - <cache-name>: name of a cache instance that has "Storage" enabled
   //  - <datasource-name>: name of a datasource instance that has "Storage" enabled
   ////////////////////////////////////////////////////////////////
   // this.sessionStorage = "memory"; 
   ////////////////////////////////////////////////////////////////
   //  CLIENT MANAGEMENT
   //  Enables/disables client management
   ////////////////////////////////////////////////////////////////
   // this.clientManagement = false; 
   ////////////////////////////////////////////////////////////////
   //  CLIENT COOKIES
   //  Enables/disables client cookies
   ////////////////////////////////////////////////////////////////
   // this.setClientCookies = true;
   ////////////////////////////////////////////////////////////////
   //  CLIENT TIMEOUT
   //  Sets the amount of time Lucee will keep the client scope alive.
   ////////////////////////////////////////////////////////////////
   // this.clientTimeout = createTimeSpan( 90, 0, 0, 0 );
   ////////////////////////////////////////////////////////////////
   //  CLIENT STORAGE
   //  Default Storage for Session, possible values are:
   // - memory: the data are only in the memory, so in fact no persistent storage
   // - file: the data are stored in the local filesystem
   // - cookie: the data are stored in the users cookie
   // - <cache-name>: name of a cache instance that has "Storage" enabled
   // - <datasource-name>: name of a datasource instance that has "Storage" enabled
   ////////////////////////////////////////////////////////////////
   // this.clientStorage = "cookie";
   ////////////////////////////////////////////////////////////////
   //  DOMAIN COOKIES
   //  Enables or disables domain cookies. 
   ////////////////////////////////////////////////////////////////
   // this.setDomainCookies = false; 
   ////////////////////////////////////////////////////////////////
   //  CGI READ ONLY 
   //  Defines whether the CGI Scope is read only or not.
   ////////////////////////////////////////////////////////////////
   // this.cgiReadOnly = true;
   ////////////////////////////////////////////////////////////////
   //  LOCAL SCOPE MODE
   //  Defines how the local scope of a function is invoked when a variable with no scope definition is used.
   //  - modern: the local scope is always invoked
   //  - classic: CFML default,  the local scope is only invoked when the key already exists in it
   ////////////////////////////////////////////////////////////////
   // this.localMode = "classic"; 
   ////////////////////////////////////////////////////////////////
   //  CASCADING  
   //  Depending on this setting Lucee scans certain scopes to find a 
   //  variable called from the CFML source. This will only happen when the 
   //  variable is called without a scope. (Example: #myVar# instead of #variables.myVar#)
   //  - strict: scans only the variables scope
   //  - small: scans the scopes variables,url,form
   //  - standard: CFML Standard, scans the scopes variables,cgi,url,form,cookie
   ////////////////////////////////////////////////////////////////
   // this.scopeCascading = "standard";
   ////////////////////////////////////////////////////////////////
   //  SEARCH RESULTSETS  
   //  When a variable has no scope defined (Example: #myVar# instead of #variables.myVar#), 
   //  Lucee will also search available resultsets (CFML Standard) or not
   ////////////////////////////////////////////////////////////////
   // this.searchResults = true;
   ////////////////////////////////////////////////////////////////
   //  REQUEST: TIMEOUT
   //  Sets the amount of time the engine will wait
   //  for a request to finish before a request timeout will 
   //  be raised. This means that the execution of the request 
   //  will be stopped. This setting can be overridden using the 
   //  "cfsetting" tag or script equivalent.
   ////////////////////////////////////////////////////////////////
   // this.requestTimeout=createTimeSpan(0,0,0,50); 
   ////////////////////////////////////////////////////////////////
   //  COMPRESSION  
   //  Enable compression (GZip) for the Lucee Response stream 
   //  for text-based responses when supported by the client (Web Browser)
   ////////////////////////////////////////////////////////////////
   // this.compression = false;
   ////////////////////////////////////////////////////////////////
   //  SUPPRESS CONTENT FOR CFC REMOTING 
   //  Suppress content written to response stream when a 
   //  Component is invoked remote
   ////////////////////////////////////////////////////////////////
   // this.suppressRemoteComponentContent = false;
   ////////////////////////////////////////////////////////////////
   //  BUFFER TAG BODY OUTPUT 
   //  If true - the output written to the body of the tag is 
   //  buffered and is also outputted in case of an exception. Otherwise
   //  the content to body is ignored and not displayed when a failure
   //  occurs in the body of the tag.
   ////////////////////////////////////////////////////////////////
   // this.bufferOutput = false; 
   ////////////////////////////////////////////////////////////////
   //  UDF TYPE CHECKING 
   //  Enables/disables type checking of definitions with 
   //  function arguments and return values
   ////////////////////////////////////////////////////////////////
   // this.typeChecking = true;
   ////////////////////////////////////////////////////////////////
   //  QUERY CHACHEDAFTER
   //  Global caching lifespan for queries. This value is overridden when
   //  a tag "query" has the attribute "cachedwithin" defined.
   ////////////////////////////////////////////////////////////////
   // this.query.cachedAfter = createTimeSpan(0,0,0,0);
   ////////////////////////////////////////////////////////////////
   //  REGEX 
   //  Defines the regular expression dialect to be used.
   //  - modern: Modern type is the dialect used by Java itself.
   //  - classic CFML default, the classic CFML tradional type Perl5 dialect
   ////////////////////////////////////////////////////////////////
   // this.regex.type = "perl";
   ////////////////////////////////////////////////////////////////
   //  IMPLICIT NOTATION
   //  If there is no accessible data member (property, element of the this scope) 
   //  inside a component, Lucee searches for available matching "getters" or 
   //  "setters" for the requested property. The following example should 
   //  clarify this behaviour. "somevar = myComponent.properyName". 
   //  If "myComponent" has no accessible data member named "propertyName", 
   //  Lucee searches for a function member (method) named "getPropertyName".
   ////////////////////////////////////////////////////////////////
   // this.invokeImplicitAccessor = false;
   ////////////////////////////////////////////////////////////////
   //  ANTI-XXE CONFIGURATION
   //  XML External Entity attack is a type of attack against
   //  an application that parses XML input. This configuration enable/disable
   //  protection by XXE attack. It's enabled by default from 5.4.2 and 6.0.
   //  https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
   ////////////////////////////////////////////////////////////////
   // this.xmlFeatures = {
   //	  externalGeneralEntities: false,
   //	  secure: true,
   //	  disallowDoctypeDecl: false
   // };
   ////////////////////////////////////////////////////////////////
   //  MAIL SERVERS 
   //  defines one or more mail server connections. 
   //  When sending an email, Lucee tries to send the mail with the first 
   //  defined mail server. If the send operation fails, Lucee will 
   //  continue using the next mail server in the list.
   ////////////////////////////////////////////////////////////////
   // this.mailservers =[
   //     {
   //         host: "smtp.somesmtp.org"
   //        ,port: 587
   //        ,username: "email@somedomain.org"
   //        ,password: "mypassword"
   //        ,ssl: false
   //        ,tls: true
   //        ,lifeTimespan: CreateTimeSpan( 0, 0, 1, 0 )
   //        ,idleTimespan: CreateTimeSpan( 0, 0, 0, 10 )
   //    } 
   // ];
   ////////////////////////////////////////////////////////////////
   //  DATASOURCES
   //  Defines datasources by datasource name. These can be addressed by 
   //  by the "datasource" attribute of a "query" tag.
   ////////////////////////////////////////////////////////////////
   // 
   //  this.datasources["myDsnName"] = {
   //         class: 'com.mysql.cj.jdbc.Driver'
   //     , bundleName: 'com.mysql.cj'
   //     , bundleVersion: '8.0.19'
   //     , connectionString: 'jdbc:mysql://localhost:3306/test?characterEncoding=UTF-8&serverTimezone=Europe/Berlin&maxReconnects=3'
   //     , username: 'root'
   //     , password: "encrypted:..."
   //     // optional settings
   //     , connectionLimit:100 // default:-1
   //     , liveTimeout:60 // default: -1; unit: minutes
   //     , alwaysSetTimeout:true // default: false
   //     , validate:false // default: false
   // };
   ////////////////////////////////////////////////////////////////
   //  CACHES
   ////////////////////////////////////////////////////////////////
   //  this.cache.connections["myCache"] = {
   //     class: 'lucee.runtime.cache.ram.RamCache'
   //   , storage: false
   //   , custom: {"timeToIdleSeconds":"0","timeToLiveSeconds":"0"}
   //   , default: ''
   // };
   ////////////////////////////////////////////////////////////////
   //  MAPPINGS   
   ////////////////////////////////////////////////////////////////
   //
   // this.mappings["/lucee/admin"]={
   //         physical:"{lucee-config}/context/admin"
   //         ,archive:"{lucee-config}/context/lucee-admin.lar"
   // };
   //
   // this.mappings["/lucee/doc"]={
   //         archive:"{lucee-config}/context/lucee-doc.lar"
   // };

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


