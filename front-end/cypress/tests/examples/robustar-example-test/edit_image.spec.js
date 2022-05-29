describe('Edit image', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/#/image-list/train');
  });

  it('Goes to image edit page', () => {
    cy.getBySel('image-list-img-1').trigger('mouseenter'); // 'mouseover' does not trigger the overlay!
    cy.getBySel('image-list-btn-edit-image-1').click();

    cy.wait(1000); // Must wait for some time here for image to load, otherwise drawing will fail!
    cy.get('.upper-canvas')
      .trigger('mousedown', 15, 15)
      .trigger('mousemove', 50, 50)
      .trigger('mouseup');

    cy.get('.tui-image-editor-send-edit-btn').click();

    cy.visit('http://localhost:8080/#/image-list/annotated');
  });
});
