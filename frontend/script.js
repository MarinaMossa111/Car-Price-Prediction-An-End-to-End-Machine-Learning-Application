console.log("✅ SCRIPT LOADED");


const API_URL = "http://127.0.0.1:8000";


// Adjust this to roughly the max realistic price in your
// dataset — it only controls how full the gauge arc looks,
// it does NOT affect the actual prediction in any way.
const GAUGE_MAX_PRICE = 2000000;


document.addEventListener("DOMContentLoaded", function(){


    const button = document.getElementById("predictButton");


    console.log("BUTTON:", button);



    loadPreviousPrediction();



    button.addEventListener(
        "click",
        predictPrice
    );

});




// ===============================
// Prediction Function
// ===============================

async function predictPrice(){


    console.log("✅ BUTTON CLICKED");


    const priceBox =
        document.getElementById("predictedPrice");


    const modelBox =
        document.getElementById("selectedModel");



    priceBox.innerHTML =
        "⏳ Predicting...";



    const data = {


        algorithm:
        document.getElementById("algorithm").value,


        car_name:
        document.getElementById("car_name").value,


        brand:
        document.getElementById("brand").value,


        car_model:
        document.getElementById("car_model").value,


        vehicle_age:
        Number(document.getElementById("vehicle_age").value),


        km_driven:
        Number(document.getElementById("km_driven").value),


        seller_type:
        document.getElementById("seller_type").value,


        fuel_type:
        document.getElementById("fuel_type").value,


        transmission_type:
        document.getElementById("transmission_type").value,


        mileage:
        Number(document.getElementById("mileage").value),


        engine:
        Number(document.getElementById("engine").value),


        max_power:
        Number(document.getElementById("max_power").value),


        seats:
        Number(document.getElementById("seats").value)

    };



    console.log("Sending:", data);



    try{


        const response = await fetch(

            API_URL + "/predict",

            {

                method:"POST",

                headers:{

                    "Content-Type":"application/json"

                },


                body:
                JSON.stringify(data)

            }

        );



        const result =
        await response.json();



        console.log(result);



        displayResult(result);



        // Save in browser

        localStorage.setItem(

            "latestPrediction",

            JSON.stringify(result)

        );



    }



    catch(error){


        console.error(error);


        priceBox.innerHTML =
        "❌ API Connection Error";

    }

}





// ===============================
// Display Result
// ===============================

function displayResult(result){


    document.getElementById("predictedPrice")
    .innerHTML =

    `
    💰 ₹ ${Number(result.predicted_price).toLocaleString("en-IN")}
    `;



    document.getElementById("selectedModel")
    .innerHTML =

    `
    🤖 Model:
    ${result.selected_model}
    `;



    updateGauge(result.predicted_price);


}





// ===============================
// Gauge Fill Logic
// ===============================

function updateGauge(price){


    const arc =
        document.getElementById("gaugeArc");


    if(!arc) return;


    const ARC_LENGTH = 283;


    let ratio =
        Math.min(price / GAUGE_MAX_PRICE, 1);


    ratio =
        Math.max(ratio, 0);


    const offset =
        ARC_LENGTH - (ARC_LENGTH * ratio);


    arc.style.strokeDashoffset = offset;

}





// ===============================
// Load Previous Result
// ===============================

function loadPreviousPrediction(){


    const saved =
    localStorage.getItem(
        "latestPrediction"
    );


    if(saved){


        const result =
        JSON.parse(saved);


        displayResult(result);


        console.log(
            "Previous prediction loaded"
        );


    }


}