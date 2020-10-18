# TestingTeslasVision
This repo is a loose collection of code and other related files to complete my B546 project for the Fall 2020 semester. The object of this project is to evaluate if I can prove Tesla vehicles have a weakness to adversarial examples.

# Milestones of the project.

1) Build and train an object detection AI model using Detectron2.

2) Run ~1000 images through the model and record the results.

3) Build an adversarial example and apply it to the ~1000 images.

4) Run the ~1000 images (with the adversarial example) applied to them through the model and record the results.

5) Take samples from both datasets and see if a Model 3 Tesla can visualize them on the touchscreen.

6) Build a hypothesis describing and theorizing why there are discrepancies between the results.
  Did Tesla fail but Detectron2 didn't? Why?
  Vice versa. Why?
  Were both affected by the adversarial example? Why? Was the black box nature of this experiment the cause of failure? Does that make the Tesla results illegitimate? 
  Were both unaffected by the adversarial example?
