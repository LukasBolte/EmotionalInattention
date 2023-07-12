"use strict";

function task(parameters){
    
    //fundamentals (coming from outside)
    this.playerID=parameters.playerID;
    console.log(parameters.root)
    this.root=document.getElementById(parameters.root);
    console.log("my highlighting")
    console.log(this.root,"my root element")
    
    this.varname=parameters.varname;
    this.sequence=JSON.parse(parameters.sequence);
    this.min_pay=parseInt(parameters.min_pay);
    this.max_pay=parseInt(parameters.max_pay);
    this.treatment=parameters.treatment;
    this.delay=parameters.delay;
    this.open_box_src=parameters.open_box_src;
    this.closed_box_src=parameters.closed_box_src;

    console.log(this.delay, 'my delay')

    console.log(this.min_pay,this.max_pay)
    this.draw=function(){
        //attach input field
        var hidden=document.createElement("input");
        hidden.setAttribute("type","hidden");
        hidden.setAttribute("id",this.varname);
        hidden.setAttribute("name",this.varname);
        this.root.appendChild(hidden);
        //attach container that can easily be reset
        var container=document.createElement("div");

        // container.setAttribute("id","container_id");
        this.root.appendChild(container);

        var div=document.createElement("div");
        div.className="row justify-content-center";
        container.appendChild(div);

        var divWidth=document.createElement("div");
        divWidth.className="col-md-6 col-lg-9";

        div.appendChild(divWidth)
        this.container = divWidth
    };

    this.drawBox=function(){
        var table=document.createElement("table");
        table.className="table no-border-table";
        this.container.appendChild(table);

        var tbody=document.createElement("tbody");
        table.appendChild(tbody);

        var tr=document.createElement("tr")
        tr.style.height = '300px'
        tbody.appendChild(tr);

        var td=document.createElement("td")
        td.setAttribute("id","row1_id")
        td.className="col-6";
        td.style.textAlign='center';
        tr.appendChild(td);

        var tr=document.createElement("tr")
        tr.style.height = '100px'
        tbody.appendChild(tr);

        var td=document.createElement("td")
        td.setAttribute("id","row2_id");
        td.style.textAlign='center';
        tr.appendChild(td);
    };

    this.load=function(){
        var keyName=this.playerID+":"+this.root;
        var savedValue=localStorage.getItem(keyName); 
        console.log(savedValue);
        this.num_draws=0;
        this.open_page="page1";
        if (savedValue!=undefined){
            this.num_draws=JSON.parse(savedValue)['num_draws'];
            this.open_page=JSON.parse(savedValue)['open_page'];
            }
            document.getElementById(this.varname).value=JSON.stringify(this.num_draws);
    };

     //storage functions
    this.save=function(){
        var keyName=this.playerID+":"+this.root;
        var output={};
        output.num_draws=this.num_draws;
        output.open_page=this.open_page;
        localStorage.setItem(keyName,JSON.stringify(output));
        document.getElementById(this.varname).value=JSON.stringify(output);
    }

    this.clearContainer=function(){
        this.container.innerHTML="";
    };

    this.draw1=function(){
        this.clearContainer();
        this.drawBox();
        var td=document.getElementById("row1_id");

        var container=document.createElement("div");
        td.appendChild(container);
        
        var table=document.createElement("table");
        table.className="table no-border-table";
        container.appendChild(table)
        var tbody=document.createElement("tbody");
        table.appendChild(tbody)
        var tr=document.createElement("tr")
        tbody.append(tr);
        var td1=document.createElement("td");
        td1.style.width="50%";



        var p=document.createElement('p');
        var bonus
        if (this.num_draws==0){
            bonus=this.min_pay;
        } else {
            bonus=Math.max(...this.sequence.slice(0,this.num_draws))
        }

        var amount
        if (this.treatment=="bonus"){
            p.innerHTML="Your bonus if you end the task now:"
            amount = bonus
        } else if (this.treatment=="penalty"){
            p.innerHTML="Your penalty if you end the task now:"
            amount = this.min_pay+this.max_pay-bonus
        }

        

        
        td1.appendChild(p);


        var p=document.createElement('p');
        p.className="h4 mt-5";
        p.innerHTML="$"+ amount.toString();

        td1.appendChild(p);
        tr.appendChild(td1)



        var td2=document.createElement("td");
        td2.style.width="50%";

        

        var p=document.createElement('p');
        p.innerHTML="Next Box:"
        td2.appendChild(p);
        var img=document.createElement('img');
        img.setAttribute("src",this.closed_box_src)
        img.className="img-fluid mb-3";
        img.style.height="70px";
        td2.appendChild(img);



        tr.appendChild(td2)
        
        var td=document.getElementById("row2_id");




        var container=document.createElement("div");
        td.appendChild(container);
        
        var table=document.createElement("table");
        table.className="table no-border-table";
        container.appendChild(table)
        var tbody=document.createElement("tbody");
        table.appendChild(tbody)
        var tr=document.createElement("tr")
        tbody.append(tr);
        var td0=document.createElement("td")
        td0.style.width="50%";
        tr.appendChild(td0)
        var td1=document.createElement("td");
        td1.style.width="25%";

        var openBoxButton=document.createElement("button")
        openBoxButton.setAttribute("type","button");
        openBoxButton.setAttribute("id","openBoxButton_id")
        openBoxButton.className="btn btn-primary";
        openBoxButton.innerHTML="Open Box ("+this.delay+"s)";
        openBoxButton.addEventListener('click', () => {
            this.startOpening();
          });
        td1.appendChild(openBoxButton);

        tr.appendChild(td1)

        var td2=document.createElement("td");
        td2.style.width="25%";

        var endTaskButton=document.createElement("button")
        endTaskButton.setAttribute("type","button");
        endTaskButton.className="btn btn-secondary";
        endTaskButton.innerHTML="End Task";
        endTaskButton.addEventListener('click', () => {
            this.draw3();
          });
        td2.appendChild(endTaskButton);

        tr.appendChild(td2)




   
    }

    this.startOpening=function(){
        console.log(this.delay)
        let seconds =this.delay-1;
        document.getElementById("openBoxButton_id").innerHTML="Open Box ("+seconds.toString()+"s)"
        console.log('printing seconds')
        console.log(seconds)
        console.log(this, 'my this element')
        // Update the timer every second
        const timerInterval = setInterval(() => {
            // Decrease the seconds by 1
          seconds--;
          console.log(seconds);
          document.getElementById("openBoxButton_id").innerHTML="Open Box ("+seconds.toString()+"s)"
  
          
  
          // Check if the timer has reached zero
          if (seconds ===  -1) {
            clearInterval(timerInterval); // Stop the timer
            this.num_draws++;
            this.open_page="page2";

            console.log(this, 'my second this element')

            this.save();

            this.draw2(); // Call the function after the timer reaches zero
          }
        }, 1000); // Interval of 1 second (1000 milliseconds)
    }
    
    this.draw2=function(){
        this.clearContainer();
        console.log("draw2 is executed")
        this.drawBox();
        var td=document.getElementById("row1_id");
        var p=document.createElement('p');
        p.innerHTML="You decided to open the box"
        td.appendChild(p);
        var img=document.createElement('img');
        img.setAttribute("src",this.open_box_src)
        img.className="img-fluid mb-3";
        img.style.height="70px";
        td.appendChild(img);
    
        console.log(this.num_draws,'number of draws heeeere')
        console.log(this.sequence, this.num_draws-1)
        var last_num= this.sequence[this.num_draws-1]
   

        var p=document.createElement('p');
        if (this.treatment=="bonus"){
            p.innerHTML="The box contains a bonus amount of $"+last_num.toString()
        } else if (this.treatment=="penalty"){
            var penalty = this.min_pay+this.max_pay-last_num
            p.innerHTML="The box contains a penalty charge of $"+penalty.toString()
        }

        
        td.appendChild(p);

        var p=document.createElement('p');
        var bonus=Math.max(...this.sequence.slice(0,this.num_draws))
   
        if (this.treatment=="bonus"){
            p.innerHTML="So your bonus if you end the task now is $"+ bonus.toString()
        } else if (this.treatment=="penalty"){
            var penalty = this.min_pay+this.max_pay-bonus
            p.innerHTML="So your penalty if you end the task now is $"+ penalty.toString()
        }

        
        td.appendChild(p);
        
        console.log('toward the end')
        var td=document.getElementById("row2_id");

        var continueButton=document.createElement("button")
        continueButton.setAttribute("type","button");
        continueButton.setAttribute("id","continueButton_id")
        continueButton.className="btn btn-primary";
        continueButton.innerHTML="Continue";
        continueButton.addEventListener('click', () => {
            this.open_page="page1";
            this.save()
            this.draw1();
          });
        td.appendChild(continueButton);
    }
    

    this.draw3=function(){
        this.clearContainer();
        console.log("draw3 is executed")
        this.drawBox();
        var td=document.getElementById("row1_id");
        var p=document.createElement('p');
        p.innerHTML="You decided to end the task"
        td.appendChild(p);
        
        var p=document.createElement('p');

        var bonus
        if (this.num_draws==0){
            bonus=this.min_pay;
        } else {
            bonus=Math.max(...this.sequence.slice(0,this.num_draws))
        }

       
        if (this.treatment=="bonus"){
            p.innerHTML="Your final bonus payment is $"+ bonus.toString()
        } else if (this.treatment=="penalty"){
            penalty = this.min_pay+this.max_pay-bonus
            p.innerHTML="Your final charge is $"+penalty.toString()
        }

            
        td.appendChild(p);

        var td=document.getElementById("row2_id");

        var nextButton=document.createElement("button")
        nextButton.setAttribute("id","nextButton_id")
        nextButton.className="btn btn-primary btn-large";
        nextButton.innerHTML="Next";
        nextButton.style.float = 'right';
        td.appendChild(nextButton);

        // <button style="float: right" class="btn btn-primary btn-large">Next</button>

    }



    this.draw();
    this.load();

    switch (this.open_page) {
        case "page1":
            this.draw1();
            break;
        case "page2":
            this.draw2();
            break;
        case "page3":
            this.draw3();
            break;
        }


    //     this.questionHook.innerHTML="";
    //     var table=document.createElement("table");
    //     table.className="table table-hover";
    //     this.questionHook.appendChild(table);
    //     var tbody=document.createElement("tbody");
    //     table.appendChild(tbody);
    //     //make ordered list for questions
    //     var order=["overall","sure1","sure2","unsure"];
    //     for(var i=0;i<order.length;i++){
    //         var q=order[i];
    //         if (q=="sure1"){
    //             this.part2Div=document.createElement("div");
    //             this.questionHook.appendChild(this.part2Div);
    //             var table2=document.createElement("table");
    //             table2.className="table";
    //             this.part2Div.appendChild(table2);
    //             var tbody2=document.createElement("tbody");
    //             table2.appendChild(tbody2);
    //             var tr =document.createElement("tr");
    //             tbody2.appendChild(tr);
    //             this.part2DivInstructions=document.createElement("td");
    //             this.part2DivInstructions.setAttribute("colspan",2);
    //             tr.appendChild(this.part2DivInstructions);
    //             if (this.sliderDetails["overall"]==undefined || this.sliderDetails["overall"].sliderValue==undefined){
    //                 this.part2Div.style.visibility="hidden";
    //             }
    //             else{
    //                 this.part2DivInstructions.innerHTML=this.subQuestionInstructions.replace("TOTAL",this.sliderDetails["overall"]["sliderValue"]);
    //                 this.part2Div.style.visibility="visible";        
    //             }
    //         }
    //         if (this.sliderDetails[q]==undefined){
    //             this.sliderDetails[q]={};
    //         }    
    //         if (this.part2Div==undefined){
    //             this.drawSingleQuestionSlider(tbody,q);    
    //         }
    //         else{
    //             this.drawSingleQuestionSlider(tbody2,q);    
    //         }
    //     }
    //     //now draw error message
    //     var table=document.createElement("table");
    //     table.className="table";
    //     this.questionHook.appendChild(table);
    //     var tbody=document.createElement("tbody");
    //     table.appendChild(tbody);
    //     var tr =document.createElement("tr");
    //     tbody.appendChild(tr);
    //     this.errorMessage=document.createElement("td");
    //     tr.appendChild(this.errorMessage);
    //     this.errorMessage.style.visibility="hidden";
    //     this.errorMessage.className="text-warning";
    // }

    // this.drawSingleQuestionSlider = function(tbody,q){
    //     var tr =document.createElement("tr");
    //     tbody.appendChild(tr);
    //     var td=document.createElement("td");
    //     tr.appendChild(td);
    //     td.className="float-right";
    //     td.innerHTML=this.questions[q].text;
    //     //now append slider
    //     td=document.createElement("td");
    //     tr.appendChild(td);
    //     td.className="w-50";
    //     var input=document.createElement("input");
    //     input.id=this.questions[q]["variable"]+"_slider";
    //     td.appendChild(input);
    //     td.innerHTML+="<br/>";

    //     this.sliderDetails[q]["note"]=document.createElement("span");
    //     td.appendChild(this.sliderDetails[q]["note"]);
    //     this.sliderDetails[q]["note"].className="font-italic";
    //     this.sliderDetails[q]["note"].innerHTML="Please make a selection";
    //     this.sliderDetails[q]["message"]=document.createElement("span");
    //     td.appendChild(this.sliderDetails[q]["message"]);
    //     this.sliderDetails[q]["message"].className="font-weight-bold";
    //     var initValue=0;
    //     if (this.sliderDetails[q]["sliderValue"]!=undefined){
    //         initValue=this.sliderDetails[q]["sliderValue"];
    //     }
    //     this.sliderDetails[q]["slider"] = new Slider("#"+input.id, {
    //         id: input.id,
    //         dataSliderId: input.id,
    //         min: 0,
    //         max: 8,
    //         step: 1,
    //         value: initValue});        
    //     var context={"context":this,"question":q}
    //     this.sliderDetails[q]["slider"].on("slideStop", function(sliderValue) {
    //         this["context"].sliderDetails[this["question"]]["sliderValue"]=sliderValue;
    //         this["context"].change(this["question"]);
    //         this["context"].save();
    //     }.bind(context));
    //     if (this.sliderDetails[q]["sliderValue"]!=undefined){
    //         this.change(q);
    //     }
    // }

    // this.change=function(q){
    //     this.sliderDetails[q]["note"].style.display="none";
    //     this.sliderDetails[q]["message"].innerHTML = this.sliderDetails[q]["sliderValue"]+" "+this.questions[q]["answerSuffix"];
    //     if (q=="overall" && this.part2Div!=undefined){
    //         this.part2DivInstructions.innerHTML=this.subQuestionInstructions.replace("TOTAL",this.sliderDetails[q]["sliderValue"]);
    //         this.part2Div.style.visibility="visible";
    //     }
    //     if (this.errorMessage!=undefined){
    //         this.errorMessage.style.visibility="hidden";
    //     }
    // }

    // this.sliderConfirmModal=null;
    // this.checkCompleteness=function(e){
    //     var order=["overall","sure1","sure2","unsure"];
    //     var total=0;
    //     var sum=0;
    //     for(var i=0;i<order.length;i++){
    //         var q=order[i];
    //         if (this.sliderDetails[q]["sliderValue"]==undefined){
    //             this.errorMessage.innerHTML=this.questions[q].missingError;
    //             this.errorMessage.style.visibility="visible";
    //             if (e!=undefined){
    //                 e.stopPropagation();
    //             }
    //             this.failedAttempts.push(this.codeFailedAttempt());
    //             this.save();
    //             return;
    //         }
    //         else{
    //             if (q=="overall"){
    //                 total=parseInt(this.sliderDetails[q]["sliderValue"]);
    //             }
    //             else{
    //                 sum=sum+parseInt(this.sliderDetails[q]["sliderValue"]);
    //             }
    //         }
    //     }
    //     if (total!=sum){
    //         this.errorMessage.innerHTML=this.subQuestionSummationError.replace("TOTAL",total);
    //         this.errorMessage.style.visibility="visible";
    //         if (e!=undefined){
    //             e.stopPropagation();
    //         }
    //         //save failed attempt
    //         this.failedAttempts.push(this.codeFailedAttempt());
    //         this.save();
    //         return;         
    //     }
    //     //now open modal
    //     this.sliderConfirmModal = new bootstrap.Modal(document.getElementById("sliderConfirmModal"), {
    //         keyboard: false
    //     });    
    //     document.getElementById("sliderConfirmModalClose1").addEventListener("click",function(evt){
    //         this.sliderConfirmModal.hide();
    //     }.bind(this));
    //     document.getElementById("sliderConfirmModalClose2").addEventListener("click",function(evt){
    //         this.sliderConfirmModal.hide();
    //     }.bind(this));
    //     document.getElementById("sliderConfirmModalNext").addEventListener("click",function(evt){
    //         document.dispatchEvent(new CustomEvent(["finishedslider"], {
    //             bubbles: true,
    //             detail: this.retrieve()
    //         }));        
    //         this.sliderConfirmModal.hide();
    //         }.bind(this));
    //     this.sliderConfirmModal.show();
    // }

    // this.codeFailedAttempt = function(){
    //     var output={};
    //     for(var q in this.questions){
    //         if (this.sliderDetails[q]==undefined || this.sliderDetails[q]["sliderValue"]==undefined){
    //             output[this.questions[q]["variable"]]="missing";
    //         }
    //         else{
    //             output[this.questions[q]["variable"]]=this.sliderDetails[q]["sliderValue"];
    //         }
    //     }
    //     //console.log(output);
    //     return output;
    // }

    // //storage functions
    // this.save=function(){
    //     var keyName=this.playerID+":"+this.rootName;
    //     var output={};
    //     output.failedAttempts=this.failedAttempts;
    //     var allDefined=true;
    //     for(var q in this.questions){
    //         if (this.sliderDetails[q]==undefined || this.sliderDetails[q]["sliderValue"]==undefined){
    //             allDefined=false;
    //         }
    //         else{
    //             output[this.questions[q]["variable"]]=this.sliderDetails[q]["sliderValue"];
    //         }
    //     }
    //     localStorage.setItem(keyName,JSON.stringify(output));
    //     document.getElementById(this.hiddenField).value=JSON.stringify(output);
    // }   

    
    // this.load=function(){
    //     var keyName=this.playerID+":"+this.rootName;
    //     var savedValue=localStorage.getItem(keyName); 
    //     //console.log(savedValue);
    //     if (savedValue!=undefined){
    //         var output=JSON.parse(savedValue);
    //         for(var q in this.questions){
    //             if (output[this.questions[q]["variable"]]!=undefined){
    //                 if (this.sliderDetails[q]==undefined){
    //                     this.sliderDetails[q]={};
    //                 }
    //                 this.sliderDetails[q]["sliderValue"]=output[this.questions[q]["variable"]];
    //             }
    //         }
    //         if (output.failedAttempts!=undefined){
    //             this.failedAttempts=output.failedAttempts;
    //         }
    //         document.getElementById(this.hiddenField).value=savedValue;
    //     }
    // }

    // this.retrieve=function(){
    //     var output={};
    //     output.failedAttempts=this.failedAttempts;
    //     var allDefined=true;
    //     for(var q in this.questions){
    //         if (this.sliderDetails[q]==undefined || this.sliderDetails[q]["sliderValue"]==undefined){
    //             allDefined=false;
    //         }
    //         else{
    //             output[this.questions[q]["variable"]]=this.sliderDetails[q]["sliderValue"];
    //         }
    //     }
    //     return output;
    // }

    // this.reset=function(){
    //     for(var q in this.questions){
    //         this.sliderDetails[q]["sliderValue"]=undefined;
    //         this.sliderDetails[q]["slider"].setValue(0);
    //         this.sliderDetails[q]["message"].innerHTML="";
    //         this.sliderDetails[q]["note"].style.display="";
    //     }
    //     this.failedAttempts=[];
    //     this.part2Div.style.visibility="hidden";
    //     this.save();
    //     this.errorMessage.style.visibility="hidden";
    // }

    // //create styles
    // for (var q in this.questions){
    //     var style = document.createElement('style');
    //     style.innerHTML = "#"+this.questions[q]["variable"]+"_slider"+" .slider-selection {background: #AAAAAA;}";
    //     document.getElementsByTagName('head')[0].appendChild(style);    
    // }
    // //attach hidden field
    // var hidden=document.createElement("input");
    // hidden.setAttribute("type","hidden");
    // hidden.setAttribute("id",this.hiddenField);
    // hidden.setAttribute("name",this.hiddenField);
    // this.questionRoot.appendChild(hidden);
    // //atach modal warning
    // var modal=`
    // <div id="sliderConfirmModal" class="modal" tabindex="-1" role="dialog">
    // <div class="modal-dialog" role="document">
    //   <div class="modal-content">
    //     <div class="modal-header">
    //       <h5 class="modal-title">Before you continue</h5>
    //       <button type="button" class="close" data-dismiss="modal" aria-label="Close" id="sliderConfirmModalClose1">
    //         <span aria-hidden="true">&times;</span>
    //       </button>
    //     </div>
    //     <div class="modal-body">
    //       <p>Are you sure about your answers? If you are, click "Next" to continue.</p>
    //     </div>
    //     <div class="modal-footer">
    //       <button type="button" class="btn btn-secondary" data-dismiss="modal" id="sliderConfirmModalClose2">Close</button>
    //       <button type="button" class="btn btn-primary" style="float:right" id="sliderConfirmModalNext">
    //         Next</button>
    //     </div>
    //   </div>
    // </div>
    // </div>`;
    // this.questionRoot.innerHTML+=modal;

    // //attach hook for question
    // this.questionHook=document.createElement("div");
    // this.questionRoot.appendChild(this.questionHook);

    // this.load();
    // this.draw();
    // this.save();

}

