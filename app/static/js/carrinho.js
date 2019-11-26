const INPUTS = $('.inpt-qnt')

for (const INPUT of INPUTS) {
    INPUT.addEventListener('change', function() {
        const quantidade_max = this.max;
        const quantidade_min = this.min;
        const quantidade = this.value;
        const indice = this.dataset.index;

        if (quantidade >= quantidade_min && quantidade <= quantidade_max) {
            const POSICAO_INPUT = getPosicaoInput(indice);

            if (POSICAO_INPUT !== -1) {
                alterarQuantidadeItem(quantidade, POSICAO_INPUT); 
            }         
        }
    });
}

const getPosicaoInput = function(indice) {
    let INDICE_OBJETO = -1;

    for (const INPUT of INPUTS) {
        INDICE_OBJETO++;

        if (INPUT.dataset.index  == indice) {
            return INDICE_OBJETO;
        }
    }

    return INDICE_OBJETO;
}

const alterarQuantidadeItem = function(quantidade, indice) {
    $.ajax({
        type: 'POST',
        url: '/carrinho/alterarquantidade',
        data: {
            'quantidade_nova': quantidade,
            'indice': indice
        }
    });
};
