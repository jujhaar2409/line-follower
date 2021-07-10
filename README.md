# Line Follower

The file main.py contains a starter environment in which you have a car and the ability to draw a path. 
Your task is to add a PID controller to control the movement of the car and make it follow the drawn path.

## Get Started

Download the file main.py from this repo and then open a terminal at the location of the file and do the following

```bash
pip install pygame
python main.py
```

## Resources

### PID refresher
You can go through this [PID Playlist](https://youtube.com/playlist?list=PLn8PRpmsu08pQBgjxYFXSsODEF3Jqmm-y) for a quick refresher on what PID control and how it is used.
You don't need to watch the whole playlist, this is just to refresh a few key concepts that will be needed.

### Python and pygame resources(optional)
- [pygame documentation](https://www.pygame.org/docs/) - Very useful for finding useful functions, specially [this](https://www.pygame.org/docs/ref/math.html#pygame.math.Vector2)
- [Pygame tutorial](https://youtu.be/FfWpgLFMI7w) - do only what is required
- [Python tutorial](https://youtu.be/_uQrJ0TkZlc) - Feel free to skip sections since we have already covered the same concepts in CS101

## Methods

Two methods of solving this problem are listed below. You can use one of them or possibly even come up with your own method to tackle this problem.

### Color Sensor Method

In this method a few, say 3(try and see if more or less work better), sensors are placed in front of the car. Each of the sensors collects data about the color below(pygame has this functionality) and based on that the car is made to turn right or left.
Watch this video for reference: [video](https://www.youtube.com/watch?v=bL0MmeQhpAQ)

### Distance Method

This method makes use of sensors to find the distance of the car from a certain reference and then the controller decides how much to turn and which direction.
Watch this video for an explanation of how a more advanced type this method works: [video](https://youtu.be/4Y7zG48uHRo)

## Attribution

<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>