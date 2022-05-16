describe('This is testing visualizer', () => {
    beforeEach(() => {
        cy.visit('image-list/train');
        cy.getBySel('image-list-img-0').trigger('mouseenter');
        cy.getBySel('image-list-btn-predict-image-0').click();
    });

    // it('Test Visualizer button', () => {
    //     cy.get('float-button').trigger('mouseenter');
    //   });
    it('Test if Visualizer pop out', () => {
        cy.getBySel('visualizer-btn').should('not.exist');
        cy.getBySel('visualizer-sheet').should('be.visible');
      });

    it('Test Model Prediction Panel', () => {
        cy.getBySel('model-prediction').click();
        cy.getBySel('model-prediction-sheet')
            .find('.num').invoke('text').then(parseFloat).should('be.lte', 1);

        let DataArr = {
            label:[],
            perc:[]
        };
        let flag = 1;
        // labels are accessed at run-time from the chart object
        cy.request('http://localhost:8080/api/predict/train/0')
            .then((res)=>{
                DataArr.label = res.body.data[0]
                DataArr.perc = res.body.data[1]
                console.log('tag', DataArr)
                for(var i=0; i<DataArr.perc.length; i++){
                    if(DataArr.perc[i]> DataArr.perc[i+1]){
                        flag = -1;
                        console.log('"tag"', '')
                    }
                }
            });


            cy.get(flag);
            
            // make sure we have a valid list with labels
            // .should('have.length.gt', 0)
            // .then(labels => {
            // labels.forEach((label, k) => {
            //     cy.get(rectangles)
            //     .eq(k)
            //     .trigger('mousemove')
            //     .wait(500)

            //     cy.get('.graph-svg-tip', { log: false }).should('contain', label)
            // })
            // })

            
        cy.getBySel('model-prediction').click();
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
  