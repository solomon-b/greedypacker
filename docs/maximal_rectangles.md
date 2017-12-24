### Maximal Rectangles Algorithm
  ![Maximal Rectangle Rendering](https://raw.githubusercontent.com/ssbothwell/greedypacker/master/static/maximal_rectangleAlgorithm-bottom_leftHeuristic.png)

  Rather then choosing a split axis like in the Guillotine Algorithm, Maximal
  Rectangles adds both possible splits to the list of FreeRectangles. This
  ensures that the largest possible rectangular areas are present in the
  FreeRectangles list at all times.  

  Because a single point in the bin can now be represented by multiple
  FreeRectangles, the list must be carefully pruned between Item insertions.
  Any FreeRectangle that intersects the area occupied by the newly inserted
  Item is split such to remove the intersection. Additionally, any
  FreeRectangle which is fully overlapped by another FreeRectangle is deleleted
  from the list.

  ```
  M = greedypacker.BinManager(8, 4, pack_algo='maximal_rectangle', heuristic='bottom_left', rotation=True)
  ```


#### Heuristic Choices
* best_shortside:
  Choose a FreeRectangle (F) where the shorter remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where min(Fw - Iw, Fh - Ih) is smallest. Ties are broken with 
  `best_long`.
* best_longside:
  Choose a FreeRectangle (F) where the longer remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where max(Fw - Iw, Fh - Ih) is smallest. Ties are broken with
  `best_shortside`.
* best_area:
  Choose the FreeRectangle with the smallest area that still fits
  the Item. Ties are broken with `best_shortside`.
* worst_shortside:
  Choose a FreeRectangle (F) where the shorter remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where min(Fw - Iw, Fh - Ih) is largest. Ties are broken with 
  `worst_long_side`.
* worst_longside:
  Choose a FreeRectangle (F) where the longer remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where max(Fw - Iw, Fh - Ih) is largest. Ties are broken with
  `worst_shortside`.
* worst_area:
  Choose the FreeRectangle with the largest area that still fits
  the Item. Ties are broken with `worst_shortside`.
* bottom_left:
  Choose the FreeRectangle where the Y coordinate of the Item's
  top side is smallest. If there is a tie, pick the choice with
  the smallest X coordinate.
* contact_point:
  Choose the FreeRectangle where the maximum amount of the Item's
  perimiter is touching either occupied space or the edges of
  the bin. Ties are brokwn with `best_shortside`.
