import React, { Component } from "react";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
import DeleteIcon from '@material-ui/icons/Delete';
import { IconButton } from '@material-ui/core';

const reorder = (list, startIndex, endIndex) => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);

  return result;
};

const grid = 8;

const getItemStyle = (isDragging, draggableStyle) => ({
  userSelect: "none",
  position: 'relative',
  padding: grid * 2,
  margin: `0 0 ${grid}px 0`,

  backgroundColor: "#2f3136",
  ...draggableStyle
});

const getListStyle = isDraggingOver => ({
  backgroundColor: "#202225",
  padding: grid,
  margin: '0 auto'
});

export class DraggableList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      items: props.items
    };
    this.props.updateSortedItems(props.items);
    this.onDragEnd = this.onDragEnd.bind(this);
  }

  onDragEnd(result) {
    // dropped outside the list
    if (!result.destination) {
      return;
    }

    const items = reorder(
      this.state.items,
      result.source.index,
      result.destination.index
    );

    this.setState({
      items
    });
    this.props.updateSortedItems(items);
  }

  deleteItem = (item) => {
    let newItems = this.state.items.filter(i => i.id !== item.id);
    this.setState({
      items: newItems
    });
    this.props.updateSortedItems(newItems);
  }


  // Normally you would want to split things out into separate components.
  // But in this example everything is just done in one place for simplicity
  render() {
    return (
      <DragDropContext onDragEnd={this.onDragEnd}>
        <Droppable droppableId="droppable">
          {(provided, snapshot) => (
            <div
              {...provided.droppableProps}
              ref={provided.innerRef}
              style={getListStyle(snapshot.isDraggingOver)}
            >
              {this.state.items.map((item, index) => (
                <Draggable key={item.id} draggableId={item.id} index={index}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      style={getItemStyle(
                        snapshot.isDragging,
                        provided.draggableProps.style
                      )}
                    >
                      <span>{item.name} - {item.id} - {item.gameMode}</span>
                      <IconButton onClick={() => this.deleteItem(item)} className="delete-icon"><DeleteIcon  /></IconButton>
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    );
  }
}
