<!DOCTYPE html>
<html>
   <head>
      <link rel="shortcut icon" type="image/png" href="icons/fav_logo.png"/>
      <link rel="stylesheet"  type="text/css" href="search_style.css"/>
      <title>Search Engine</title>
   </head>

   <?php
   session_start();
   ini_set('max_execution_time', 300);
	//________________________________PhP_Code_____________________________________________
		$outputList = '';
		$paginationDisplay='';

		$dir='';//////////////////////////DIRECTORY OF PROJECT
		$pythonDir='python3';//////////////////////////DIRECTORY OF PYTHON
	 	 
		if (isset($_SESSION["LAST_ACTIVITY"]) && (time() - $_SESSION["LAST_ACTIVITY"] > 60)) {
			session_destroy();  
			session_unset();  
			header('Location:/index.php');//////////////////////////FIRST PAGE OF THE SITE
			die;
		}
		$_SESSION['LAST_ACTIVITY'] = time();
   		$directory = $dir."uploads/";
		$filecount = 0;
		$files = glob($directory . "*");
		if ($files){
			$filecount = count($files);
		}
	?>
      <div class = "panel">
         <img id = "logo" src="icons/logo.gif">
         <div class = "searchpanel">
		 <form action="" enctype="multipart/form-data" method="post">
            <input type = "text" id = "searchText" name = "searchText" placeholder = " Search here" class = "s" required></>
            <button id = 'sbtn' name = "search">Go</button>
            <div class="tooltip">
            <select id="search_op" name="search_op" class = "op" onchange="display_num()">
               <option value="Vector">Vector search</option>
               
               <option value="Bolean">Boolean search</option>

            </select>
            <span class="tooltiptext">In boolean you have to use one of the following: AND, OR, NOT</span>
		</div>
            <div class="tooltip">
            <input type = "number" id="search_num" name = "search_num" placeholder = "10" min ="1" max = "<?php echo $filecount; ?>" class = "n">
            <span class="tooltiptext">The number of results you desire </span>
		</div>
         </div>
         
         	<div class = "PRbox">
					<input type="checkbox" name="pagerank" id="check" value='1'>
					<div class="tooltip">
					<p id="checktxt">Page Rank</p>

			<span class="tooltiptext">If selected the search will take place only on websites, not files</span>
		</div>
			</div>
		 </form>
         <form action="" enctype="multipart/form-data" method="post">
            <div class = "searchpanel">
               <button type=button onclick="display('upload','Up','crawl','Cr')" id = 'ubtn'>Upload File</button>
               <input id='upload' name="upload[]" type="file" multiple="multiple" class = "u" required></>
               <div class="tooltip">
               <button id = 'Up' name="upload">Upload</button>
               <span class="tooltiptext">Only acceptable type of files is .txt</span>
		</div>
			   <p id = 'result1' ></p>	 
            </div>
         </form>
         <form action="" enctype="multipart/form-data" method="post">
            <div class = "searchpanel">
               <button type=button onclick="display('crawl','Cr','upload','Up')" id = 'cbtn'>Crawl</button>
               <input id='crawl' type = "text" name = "CrawlUrl" placeholder = " Add URL here" class = "c" required></>
               <button id = 'Cr' name="crawl">Start</button>
			   <p id = 'result2' ></p>	
            </div>
		 </form>
      </div>
      <form action="" enctype="multipart/form-data" method="post">
	  <div id = "pagepanel">
			<button name = "feed" id = 'fback'>I'm not happy with the results</button>
			<hr/>
	  </div>
	  </form>
   </body>
   <script type="text/javascript">
//_______________________________JavaScript_Code_____________________________________________

		 //(Dis)Appears number for search
		 function display_num(){
			var x = document.getElementById("search_op").value;
			var num = document.getElementById("search_num");
			if (x === 'Vector'){
				num.style.display = 'inline-block';
			}
			else{
				num.style.display = 'none';
			}
		 }
		 
         // (Dis)Appears elements
         function display(a,b,c,d){
			 var element = document.getElementById(a);
			 if(element.style.display === 'none'){
			 element.style.display = 'inline-block';
			 var element = document.getElementById(b).style.display = 'inline-block';
			 var element = document.getElementById(c).style.display = 'none';
			 var element = document.getElementById(d).style.display = 'none';
			 }
			 else{
			 element.style.display = 'none';
			 var element = document.getElementById(b).style.display = 'none';
			 }
			 //Hide result message if exist
			 var element = document.getElementById('result1').innerHTML = "";
			 var element = document.getElementById('result2').innerHTML = "";
		}
		
		// (Dis)Appears upload message 
         function uploaded(){
			var element = document.getElementById('result1').innerHTML = "Uploaded successfully";
         }
		 
		// (Dis)Appears crawl message 
		 function crawled(){
			var element = document.getElementById('result2').innerHTML = "Crawled successfully";
		 }
		 
		 function fback(){
			var element = document.getElementById('pagepanel').style.display = 'inline-block';
		 }
		 
		 //On pageload hide everything
	     var element = document.getElementById('pagepanel').style.display = 'none';
         var element = document.getElementById('Up').style.display = 'none';
         var element = document.getElementById('Cr').style.display = 'none';
         var element = document.getElementById('upload').style.display = 'none';
         var element = document.getElementById('crawl').style.display = 'none';	
      </script>
	<?php
		//When upload button is clicked
	   if(isset($_POST['upload'])){
		   if(count($_FILES['upload']['name']) > 0){
			   //Loops through each file
			   for($i=0; $i<count($_FILES['upload']['name']); $i++) {
				 if ($_FILES['upload']['type'][$i] == 'text/plain'){
				 //Gets the temp file path
				   $tmpFilePath = $_FILES['upload']['tmp_name'][$i];
	   
				   //Make sure we have a filepath
				   if($tmpFilePath != ""){

					   //Saves the filename
					   $shortname = $_FILES['upload']['name'][$i];
	   
						$fi = new FilesystemIterator("uploads", FilesystemIterator::SKIP_DOTS);
						$docId=iterator_count($fi);
						//Saves the url and the file
						$filePath = "uploads/" . $docId.'_idUPLOAD'.$_FILES['upload']['name'][$i];
	   
					   //Uploads the file into the temp dir
					   if(move_uploaded_file($tmpFilePath, $filePath)) {
						   $files[] = $shortname;
					   }
					   //To call create index
					   $_SESSION["changedFiles"]=1;
						//Show success message
						echo "<script> uploaded(); </script>";
					}
				}
			}
			}
		}
		//When crawl button is clicked
		if(isset($_POST['crawl'])){
				$url = $_POST['CrawlUrl'];
				//Calls PYTHON file
				$command = escapeshellcmd($pythonDir.' '.$dir.'crawler.py '.$url.' '.$dir);
				$res = shell_exec($command);
				//To call create index
				$_SESSION["changedFiles"]=1;
				//Shows success message
				echo "<script> crawled(); </script>";
		}
		//If no files were added
		if(!isset($_SESSION["changedFiles"])){
			$_SESSION["changedFiles"]=0;
		}
		//When search button clicked
		if(isset($_POST['search'])){
			//Calls create index if there is any change in the files
			if($_SESSION["changedFiles"]==1){
				$command = escapeshellcmd($pythonDir.' '.$dir.'createIndex.py '.$dir);
				$res = shell_exec($command);
			}
			session_unset();
			$_SESSION["changedFiles"]=0;//No change
			if ( ! empty($_POST['searchText'])){
				$pageRank=0;
				if(isset($_POST['pagerank'])){
					//Calls page rank if the necessary files exist
					if ((file_exists($dir.'crawlSet.npy'))&&(file_exists($dir.'crawlURLrelations.npy'))) {
    					$command = escapeshellcmd($pythonDir.' '.$dir.'pagerank.py '.$dir);
						$result = shell_exec($command);
						$pageRank=1;
					}//Otherwise does nothing and continue
				}

				$s = $_POST['searchText'];
				$_SESSION["query"]=$s;
				if ( ! empty($_POST['search_num'])){
					$n = $_POST['search_num'];
				}
				else{//If user did't gave number
					if($filecount > 10){
						$n = 10; //show 10
					}
					else{
						$n = $filecount; //show all the files
					}
				}
				$_SESSION["number"]=$n;
				
				$op = $_POST['search_op'];
				$_SESSION["pr"]=$pageRank;
				$_SESSION["feedback"]='none';
				if($op=="Vector"){//If type vector was choosed
					$_SESSION["option"]=0;
					$command = escapeshellcmd($pythonDir.' '.$dir.'query.py "'.$s.'" '.$n.' '.$dir.' '.$pageRank);
					$result = shell_exec($command);
				}
				else{//If type boolean was choosed
					$_SESSION["option"]=1;
					$command = escapeshellcmd($pythonDir.' '.$dir.'boolean_query.py "'.$s.'" '.$dir.' '.$pageRank);
					$result = shell_exec($command);
				}
				$result_array=json_decode($result,true);
				$result_array=$result_array['list'];
				$_SESSION["array"] = $result_array;
				//Shows feedback button
				echo "<script> fback()(); </script>";	
			}
		}	
		
		//When feedback button is clicked
		if (isset($_POST['feed'])){
			$query = $_SESSION["query"];
			$number = $_SESSION["number"];
			$option = $_SESSION["option"];
			$files = $_SESSION["array"];
			$pageR=$_SESSION["pr"];

			$list=base64_encode(json_encode($files));
			$command = escapeshellcmd($pythonDir.' '.$dir.'feedback.py '.$list.' '.$option.' '.$dir.' '.$number.' "'.$query.'" '.$pythonDir." ".$pageR);
			$result = shell_exec($command);
			$_SESSION["feedback"]='boolean';
			if($option == 0){
				$_SESSION["feedback"]='vector';
			}
			$result_array=json_decode($result,true);
			$result_array=$result_array['list'];
			$_SESSION["array"] = $result_array; 
		}
		

		//To show the results
		if (isset($_SESSION["array"])){
				$result_array=$_SESSION["array"] ;
				$nr = count($result_array);
				if (isset($_GET['pn']) ) { // Get pn from URLs vars if it was defined before
					$pn = preg_replace('#[^0-9]#i', '', $_GET['pn']); //Filter everything but numbers for security
				} else { // If it wasn't defined
					$pn = 1;
				}

		//Set number of results per page
          $itemsPerPage = 10;
          //Set total number of pages
          $lastPage = ceil($nr / $itemsPerPage);
		  if($lastPage==0){
			$lastPage=1;
		  }
          if ($pn < 1) { // If it is less than 1
            $pn = 1; // force if to be 1
          } else if ($pn > $lastPage) { //If it is greater than $lastpage
            $pn = $lastPage; //Force it to be $lastpage's value
          }
          $centerPages = "";
          $sub1 = $pn - 1;
          $sub2 = $pn - 2;
          $add1 = $pn + 1;
          $add2 = $pn + 2;
		  if ($pn == 1) {//If we are on the first page show a button to the second
            $centerPages .= '&nbsp; <span class="pagNumActive">' . $pn . '</span> &nbsp;';
            $centerPages .= '&nbsp; <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $add1 . '">' . $add1 . '</a> &nbsp;';
          } else if ($pn == $lastPage) {//If we are in the last page show a button to the last-1 page
            $centerPages .= '&nbsp; <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $sub1 . '">' . $sub1 . '</a> &nbsp;';
            $centerPages .= '&nbsp; <span class="pagNumActive">' . $pn . '</span> &nbsp;';
          } else if ($pn > 2 && $pn < ($lastPage - 1)) {//Show two previous pages and two next pages
            $centerPages .= '&nbsp; <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $sub2 . '">' . $sub2 . '</a> &nbsp;';
            $centerPages .= '&nbsp; <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $sub1 . '">' . $sub1 . '</a> &nbsp;';
            $centerPages .= '&nbsp; <span class="pagNumActive">' . $pn . '</span> &nbsp;';
            $centerPages .= '&nbsp; <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $add1 . '">' . $add1 . '</a> &nbsp;';
            $centerPages .= '&nbsp; <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $add2 . '">' . $add2 . '</a> &nbsp;';
          } else if ($pn > 1 && $pn < $lastPage) {//Show one previous page and one next page
            $centerPages .= '&nbsp; <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $sub1 . '">' . $sub1 . '</a> &nbsp;';
            $centerPages .= '&nbsp; <span class="pagNumActive">' . $pn . '</span> &nbsp;';
            $centerPages .= '&nbsp; <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $add1 . '">' . $add1 . '</a> &nbsp;';
          }
          // Get 10 results from the list
          $limit1 = ($pn - 1) * $itemsPerPage ;
		  $limit2=$itemsPerPage;
		  $newResult= array_slice($result_array, $limit1, $limit2);
		 
		  $paginationDisplay = ""; // Initialize the pagination output variable
          // If we have only one page there is no need to show pagination buttons
          if ($lastPage != "1"){

            // If we are not on page 1 we can place the Prev button
            if ($pn != 1) {
              $previous = $pn - 1;
              $paginationDisplay .=  '&nbsp;  <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $previous . '"> Prev</a> ';
            }
            // Lay in the clickable numbers display here between the Back and Next links
            $paginationDisplay .= '<span class="paginationNumbers">' . $centerPages . '</span>';
            // If we are not on the very last page we can place the Next button
            if ($pn != $lastPage) {
              $nextPage = $pn + 1;
              $paginationDisplay .=  '&nbsp;  <a class="navigationButtons" href="' . $_SERVER['PHP_SELF'] . '?pn=' . $nextPage . '"> Next</a> ';
            }
          }
          //___________________________________________DISPLAY RESULTS SETUP__________________________________
		  //Fill a list with all the results
          $outputList = '';
		  //For each result
		  if($_SESSION["feedback"]!='boolean'){
          foreach($newResult as $row){
			  $file_data = array_slice(file($dir.'uploads/'.$row[0]), 0, 1);
			  if(substr( $file_data[0], 0, 4 ) === "http"){//If it is a webpage show the url and add a link to it
						$outputList .= '<li><a href="'.$file_data[0].'" target="_blank" style="text-decoration:none; color:inherit;">'.$file_data[0].'</a></li>'; //show the link for the site
					}else{//Else show the name of the file and add a link to the content of the file
						$d=strstr( $row[0],"_idUPLOAD");
						$d=str_replace("_idUPLOAD", "", $d);
						$d=strstr( $d,".txt",true);
						$outputList .= '<li><a href="uploads/'.$row[0].'" target="_blank" style="text-decoration:none; color:inherit;">'.$d.'</a></li>';	// Show all files
					}
			   
		  }
		}else{//If the results came from boolean feedback sho just words 
		echo "<p id='bf'>You may want to add those words in your search</p>";
				
			   foreach($newResult as $row){
					$outputList .= '<li><a target="_blank" style="text-decoration:none; color:inherit;">'.$row[0].'</a></li>';	// Show all files
		  }
		  }
				}
	?>
	<div class="paginationDisplay" ><?php echo $paginationDisplay; ?></div>
        <div class="commentsDisplay" ><?php print "$outputList"; ?></div>
        <div class="paginationDisplay"><?php echo $paginationDisplay; ?></div>
		  </body>
</html> 
