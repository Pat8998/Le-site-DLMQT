fetch('loginscript?login='+encodeURIComponent(prompt("Login"))).then(
    Response => {
        Response.text().then (text => {        
            if (text=='Login OK') {
            // Redirect to a relative URL
            console.log("LoginOK")
            window.location.href = "..";
            

        } else {
            window.location.replace("https://www.youtube.com/watch?v=dQw4w9WgXcQ");
            console.log(text)
        }

        }

        )

    }
)