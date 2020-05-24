"use strict";

let brain;
let isFinished = false;

function setup() {
  createCanvas(640, 480);

  const options = {
    inputs: 34,
    outputs: 4,
    task: 'classification',
    debug: true,
  }
  brain = ml5.neuralNetwork(options);
  // Load gathered data from a json file.
  brain.loadData('data/data.json', dataReady);
}

// Call when data is loaded.
function dataReady(){
  brain.normalizeData();
  brain.train({epochs: 50}, finished);
}

// Save trained model.
function finished(){
  console.log('[DEBUG]: Model trained') ;
  brain.save();
  isFinished = true;
}


function draw(){
  // If model training is finished draw text.
  if (isFinished){
    fill(250, 0 , 255);
    noStroke();
    textSize(36);
    textAlign(CENTER, CENTER);
    text('Wytrenowano model!', width/2, height/2);
  }
}
