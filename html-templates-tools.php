<?php
/**
 * Created by PhpStorm.
 * User: naikorasu
 * Date: 06/08/19
 * Time: 23.59
 */
?>

<!DOCTYPE html>
<html>
<head>
    <script src="./node_modules/jquery/dist/jquery.min.js"></script>
    <script src="./node_modules/tinymce/tinymce.min.js"></script>
    <script>
        tinymce.init({
            selector: '#mytextarea',
            plugins: 'save print preview fullpage searchreplace autolink directionality code paste visualblocks visualchars fullscreen image imagetools link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern help',
            toolbar: 'formatselect | save | bold italic strikethrough forecolor backcolor permanentpen formatpainter | link image media pageembed | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent | removeformat | addcomment',
            paste_data_images: false,
            height: 650,
            save_onsavecallback: function () { console.log('Saved'); },
            images_dataimg_filter: function(img) {
                return img.hasAttribute('internal-blob');
            },
        });
    </script>

    <style>
        .display-base64 {
            width: 99%;
            height: 50px;
            border: 3px solid #cccccc;
            padding: 5px;
            font-family: Tahoma, sans-serif;
            background-position: bottom right;
            background-repeat: no-repeat;
        }
        /*
        .display-html {
            width: 99%;
            height: 220px;
            border: 3px solid #cccccc;
            padding: 5px;
            font-family: Tahoma, sans-serif;
            background-position: bottom right;
            background-repeat: no-repeat;
        }
        */
        body {
            background: rgb(221,245,255);
            background: linear-gradient(90deg, rgba(221,245,255,1) 0%, rgba(205,241,254,0.8057598039215687) 50%, rgba(221,245,255,1) 100%);
        }
    </style>
</head>

<body>
<form action="./html-templates-tools-process.php" method="post">
    <h3>1. Please put your image here :</h3>
    <input type="file" id="fileto64" name="fileto64">
    <h3>2. This is your base64 image result :</h3>
    <button type="button" onclick="copyToClipboard()">Copy Result to Clipboard</button>
    <textarea class="display-base64" id="disp_tmp_path"></textarea>
    <!--<h3>Edit your html design here : (Press Ctrl + Shift + F to Enable and Disable Fullscreen Mode )</h3>-->
    <h3>3. Edit your html design here :</h3>
    <textarea id="mytextarea" name="mytextarea"></textarea>
    <!--
    <button type="button" onclick="getTextAreaContent()">Get Content</button>
    <h3>This is your html Code :</h3>
    <textarea class="display-html" id="display_html"></textarea>
    -->
    <hr/>
    <button style="width: 100%; background-color: #DD4A68; color: #ffffff;" type="submit">SAVE</button>
</form>
<script>
    $('#fileto64').change( function(event) {
        var tmppath = URL.createObjectURL(event.target.files[0]);

        toDataUrl(tmppath, function(base64Img){
            $("#disp_tmp_path").html('&lt;img width="100%" src="'+base64Img+'"&gt;');
        });


    });

    function toDataUrl(src, callback, outputFormat) {
        // Create an Image object
        var img = new Image();
        // Add CORS approval to prevent a tainted canvas
        img.crossOrigin = 'Anonymous';
        img.onload = function() {
            // Create an html canvas element
            var canvas = document.createElement('CANVAS');
            // Create a 2d context
            var ctx = canvas.getContext('2d');
            var dataURL;
            // Resize the canavas to the original image dimensions
            canvas.height = this.naturalHeight;
            canvas.width = this.naturalWidth;
            // Draw the image to a canvas
            ctx.drawImage(this, 0, 0);
            // Convert the canvas to a data url
            dataURL = canvas.toDataURL(outputFormat);
            // Return the data url via callback
            callback(dataURL);
            // Mark the canvas to be ready for garbage
            // collection
            canvas = null;
        };
        // Load the image
        img.src = src;
        // make sure the load event fires for cached images too
        if (img.complete || img.complete === undefined) {
            // Flush cache
            img.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==';
            // Try again
            img.src = src;
        }
    }

    function getTextAreaContent() {
        // Get the HTML contents of the currently active editor
        //tinyMCE.activeEditor.getContent();

        // Get the raw contents of the currently active editor
        //tinyMCE.activeEditor.getContent({format : 'raw'});

        // Get content of a specific editor:
        //tinyMCE.get('content id').getContent()

        var content = tinyMCE.get('mytextarea').getContent({format : 'text'});
        $("#display_html").html(content);

    }

    function copyToClipboard() {
        /* Get the text field */
        var copyText = document.getElementById("disp_tmp_path");

        /* Select the text field */
        copyText.select();

        /* Copy the text inside the text field */
        document.execCommand("copy");

        /* Alert the copied text */
        //alert("Copied the text: " + copyText.value);
    }


</script>
</body>
</html>