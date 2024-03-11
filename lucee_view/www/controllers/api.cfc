component restpath="/api" {

    function getHelloWorld() httpMethod="GET" restpath="/hello" {
        restSetResponse({
            "status": 200,
            "content": "Hello, World!",
            "contentType": "application/json"
        });
    }

}
