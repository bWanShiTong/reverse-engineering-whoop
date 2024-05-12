# General notes

* I am not fully sure how whoop decides to measure Sp02, when Sp02 is measured red light is turned, currently I think it is measured after you sleep for certain amount, and it is measured once. From examining decompiled apk there might be a trigger to measure oxygen.

* Temperature and Respiratory Rate are measured constantly but not updated.

Test to measure points from above, after sleeping remove sleep from app, and then start new sleep after 15 minutes you can see in app under recovery that temperature is measured and different from one in sleep, while no Sp02 is measured


