const { _ } = Cypress
describe('This is testing visualizer', () => {
    beforeEach(() => {
        cy.visit('image-list/train').wait(500);
        cy.getBySel('image-list-img-0').trigger('mouseenter').wait(500);
        cy.getBySel('image-list-btn-predict-image-0').click().wait(500);
    });

    // it('Test Visualizer button', () => {
    //     cy.get('float-button').trigger('mouseenter');
    //   });
    it('Test if Visualizer pop out', () => {
        cy.getBySel('visualizer-btn').should('not.exist');
        cy.getBySel('visualizer-sheet').should('be.visible');
      });

    it('Test Model Prediction Panel', () => {
        cy.getBySel('model-prediction').click()
        cy.getBySel('model-prediction-sheet')
            .find('.num').invoke('text').then(parseFloat).should('be.lte', 1).wait(500)

        let DataArr = {
            label:[],
            perc:[]
        };            
        cy.get('li:nth-child(1)')
        cy.request('http://localhost:8080/api/predict/train/0')
            .then((res)=>{
                DataArr.label = res.body.data[0]
                DataArr.perc = res.body.data[1]
                var down = 0
                var up = 0
                for(let i=0; i<DataArr.perc.length-1; i++){
                    cy.getBySel(`item-${i}`).invoke('attr', 'title')
                        .then((res)=>{
                            up = parseFloat(res)
                            
                            cy.getBySel(`item-${i}`).parent().next().children(`[data-test=item-${i+1}]`).invoke('attr', 'title')
                                .then((res)=>{
                                    down = parseFloat(res)
                                    expect(up).to.be.least(down)
                                })
                        })
                }
            });
    });

    it('Test Model Focus Panel', () => {
        cy.getBySel('model-focus').click();
        cy.getBySel('model-focus-panel').should('be.visible');
        cy.getBySel('model-focus').click();
    });

    it('Test Influence Images', () => {
        cy.getBySel('influence-images').click();
        cy.getBySel('influence-images-panel').should('be.visible');
        cy.getBySel('influence-images').click();
    });  

    it('Test Proposed annotation Panel', () => {
        cy.getBySel('proposed-annotation').click();
        cy.getBySel('proposed-annotation-panel').should('be.visible');
        cy.getBySel('proposed-annotation').click();
    });    

    it('Test single page panel expansion/closing', () => {
        cy.getBySel('model-prediction').click();
        cy.getBySel('model-prediction-sheet').should('be.visible');
        cy.getBySel('model-focus').click();
        cy.getBySel('model-focus-panel').should('be.visible');
        cy.getBySel('influence-images').click();
        cy.getBySel('influence-images-panel').should('be.visible');
        cy.getBySel('influence-images').click();
        cy.getBySel('influence-images-panel').should('not.visible');
        cy.getBySel('proposed-annotation').click();
        cy.getBySel('proposed-annotation-panel').should('be.visible');

        it('Test the expansion/closing of panels during image conversion', () => {
            cy.getBySel('image-list-img-1').trigger('mouseenter');
            cy.getBySel('image-list-btn-predict-image-1').click();

            cy.getBySel('model-prediction-sheet').should('be.visible');
            cy.getBySel('model-focus-panel').should('be.visible');
            cy.getBySel('influence-images-panel').should('not.visible');
            cy.getBySel('proposed-annotation-panel').should('be.visible');
        })

        it('Test the expansion/closing of panels during page conversion', () => {
            cy.visit('image-list/test');
            cy.getBySel('image-list-img-1').trigger('mouseenter');
            cy.getBySel('image-list-btn-predict-image-1').click();

            cy.getBySel('model-prediction-sheet').should('be.visible');
            cy.getBySel('model-focus-panel').should('be.visible');
            cy.getBySel('influence-images-panel').should('not.visible');
            cy.getBySel('proposed-annotation-panel').should('be.visible');
        })

    });        

      
});
  