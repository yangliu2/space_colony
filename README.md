# Origin
I started to have the idea when I was listening to the book series, murder bot. It was inspiring to think about what space travel in the future might be like. Of course, this is not the first book about space travel, the most famous being star wars series. But this one stuck somehow. And I was just thinking about why I liked physics when I was little.   

One thing after another, I started to ask LLM what's the most likely space expansion route in the near future. The discussion came out that moon and mars are the most likely next target. Not teraforming, but contained pods on those places. However, another possibility have a big advantage. [O'Neill cylinder](https://en.wikipedia.org/wiki/O%27Neill_cylinder) have the promise to have 1.0 gravity, which have a lot of advantages, from bone density to human developement.  

So then I started to ask questions about how possible is the cylinder structure and what we need to build it. I first thought about doing hard calculus and quantum physic classes. But quickly realize that it's mostly for theoretical physics and not going to be rewarding for me to keep going. I probably be better off to make models and solve stuff I know. Think like what condition would human be comfortable living in. 

# Goal
So this repository will be dealing with practical issues regarding surviving on a O'Neill cylinder, and other issues related to space expansion. 

# Folder Structure
* [plan](plans/) - documents regarding concepts and ideas
  * [space_habitat_study_plan.md](plans/space_habitat_study_plan.md) - study plan of what to build
  * [issues.md](plans/issues.md) - issues to be solved or managed by models
  * [centripetal_acceleration.md](plans/centripetal_acceleration.md) - explanation of centripital acceleartion and simulation of gravity
  * [intuition_angular_velocity.md](plans/intuition_angular_velocity.md) - intuitions of angular velocity
  * [intuition_centripetal_acceleration.md](plans/intuition_centripetal_acceleration.md) - intutions of centripetal acceleration and derivations
  * [intuition_artificial_gravity.md](plans/intuition_artificial_gravity.md) - intution of how is artifical gravity generated using newton's second law.
  * [general_relativity_and_artificial_gravity.md](plans/general_relativity_and_artificial_gravity.md) - if you ever wondered why equations are all classical Newton formulas, and if modern physics around gravity affect anything, here are some questions and explanations
  * [constraint_vestibular.md](plans/constraint_vestibular.md) - deep dive into effects related to vestibular contraint for humans. Including possible ways to mitigate it and author's past history on vestibular research with Dr. Thomas A. Houpt
  * [constraint_gravity_gradient.md](plans/constraint_gravity_gradient.md) - deep dive for gravity gradient, basically the head and toe gravity difference. Not a limiting constraint
  * [constraint_cross_coupling.md](plans/constraint_cross_coupling.md) - deep dive for cross coupling, the combined effect of cylindar rotation and head rotation in daily activity. This might be most limiting constraint for human comfort. 
  * [constraint_coriolis.md](plans/constraint_coriolis.md) - deep dive on Coriolis, the real life of having additional forces perpendicular to the simulated gravity direction. Also included speculations for how people born on that system would understand physics. 
  * [constraint_gravity_minimum.md](plans/constraint_gravity_minimum.md) - another deed dive on minimal gravity required for habitation. Because achieving 1g is not a limiting constraint, it should be the default option. 
  * [constraint_rim_speed.md](plans/constraint_rim_speed.md) - talks about the upper limit of cylinder because of the rim speed and structural limit due to material engineering
* [models](models/) - physical models of limits of what may not work
  * [todos.md](models/todos.md) - list of models to make
* [conclusions](conclusions/) - distilled rules from physical models
