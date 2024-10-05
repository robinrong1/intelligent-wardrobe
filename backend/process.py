from typing import Generator, List, ByteString

# TODO: Have not chosen type for clothing yet
def edit_frame_for_clothes(frames: Generator[List[ByteString], None, None], clothes) -> Generator[List[ByteString], None, None]:
    for frame in frames:
        yield frame

# TODO: Create the markers for the clothers for the pasting
def create_marker_for_clothes(clothes):
    pass

# TODO: Find the markers on the person
def find_marker_on_person(frame: List[ByteString]):
    pass
