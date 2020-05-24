"use strict";

let video;
let poseNet;
let pose;
let skeleton;
let minimumScore = 0.75;

let brain;

let state = 'waiting';
let targetLabel;


function keyPressed(){
  let preparationTime = 5000;
  let collectingTime = 10000;

  // Save gathered data.
  if (key == 's'){
    brain.saveData();
  } else {
    // Used pressed letter as label for collected data.
    targetLabel = key;

    console.log('[INFO]: Waiting for collecting data.');
    console.log(`[INFO]: Data collecting for label: ${targetLabel}.`);

    // Prepare to collecting data.
    setTimeout(function(){
      state = 'collecting';
      console.log('[INFO]: Collecting data from camera.');
      // Stop collecting.
      setTimeout(function(){
        state = 'waitiing';
        console.log('[INFO]: Stop collecting data from camera.');
      }, collectingTime);
    }, preparationTime);
  }
}

function setup() {
  // Run camera
  createCanvas(640, 480);
  video = createCapture(VIDEO);
  video.hide();

  // Load PoseNet model
  poseNet = ml5.poseNet(video, 'single', callback);
  poseNet.on('pose', poseReceiver);

  // Create network to gather data. As input it gets output from PoseNet model.
  // As result return one of four letter labels.
  const options = {
    inputs: 34,
    outputs: 4,
    task: 'classification',
    debug: true,
  }
  brain = ml5.neuralNetwork(options);
}

// Execute when pose is caught.
function poseReceiver(poses) {
  // console.log(poses);

  if (poses.length > 0) {
    // Set pose and skeleton to global variable to draw them on canvas.
    pose = poses[0].pose;
    skeleton = poses[0].skeleton;

    if (state == 'collecting'){
      // Set inputs
      let inputs = [];
      for (let i=0; i < pose.keypoints.length; i++){
        let x = pose.keypoints[i].position.x;
        let y = pose.keypoints[i].position.y;
        inputs.push(x);
        inputs.push(y);
      }

      // Set target
      let target = [targetLabel];

      brain.addData(inputs, target);
    }
  }
}

function draw() {
  image(video, 0, 0);

  // Draw keypoints as dots.
  if (pose) {
    drawKeypoints();
  }

  // Draw skeleton(lines between dots).
  if (skeleton){
    drawSkeleton();
  }
}

function drawKeypoints(){
  for (let i = 0; i < pose.keypoints.length; i++) {
      let keypoint = pose.keypoints[i];

      // Draw yellow dot with purple frame if prediction score is above required minimum.
      if (keypoint.score > minimumScore) {
        fill(255, 255, 0);
        stroke('purple');
        strokeWeight(3);
        ellipse(keypoint.position.x, keypoint.position.y, 15);
      }
    }
}

function drawSkeleton() {
  for (let j = 0; j < skeleton.length; j++) {
    let partA = skeleton[j][0];
    let partB = skeleton[j][1];

    // Draw green line if prediction score is above required minimum.
    if(partA.score > minimumScore && partB.score > minimumScore){
      stroke(0, 255, 0);
      strokeWeight(3);
      line(partA.position.x, partA.position.y, partB.position.x, partB.position.y);
    }
  }
}

function callback() {
  console.log('[DEBUG]: PoseNet model loaded');
}