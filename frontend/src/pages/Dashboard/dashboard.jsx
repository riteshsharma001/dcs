import React, { useState } from 'react';
import
{
  FormControl,
  Grid2,
  Box,
  Typography,
} from '@mui/material';
import DcsAutocomplete from '../../components/autoComplete/DcsAutocomplete.js';
import DcsConfirmationDialog from '../../components/confirmation-dialog/DcsConfirmationDialog.js';
import DcsPageLoader from '../../components/loader/DcsPageLoader';
import DcsCreatedInfo from '../../components/template-info/DcsCreatedInfo.js';
import RentalAgreement from '../../components/Agreements/Rental_agreement.jsx';
import Cookies from 'js-cookie';
import usePricingStore from "../../store/pricingStore";

function Dashboard ()
{
  const templateTypes = [
    {
      title: 'Sale Deed',
      id: 'Sale Deed'
    },
    {
      title: 'House Rental',
      id: 'House Rental'
    }
  ];
  const [ loading, setLoading ] = useState( false );
  const [ selectedValue, setSelectedValue ] = useState( '' );
  const [ editorHtml, setEditorHtml ] = useState( '' );
  const [ dialogOpen, setDialogOpen ] = useState( false );
  const storedUser = Cookies.get( 'user' );
  const initialUser = storedUser ? JSON.parse( storedUser ) : null;
  const { selectedPricing } = usePricingStore();
  console.log(selectedPricing)
  const handleChange = ( event, newValue ) =>
  {
    if ( newValue == null )
    {
      setEditorHtml( '' );
      return;
    }
    setSelectedValue( newValue );

      if ( newValue != null )
        setDialogOpen( true );

  };
  const handleCloseDialog = () =>
  {
    setDialogOpen( false );
  };
  const handleConfirm = () =>
  {
    setEditorHtml( null );
    fetchHtml( selectedValue.title );
    setDialogOpen( false );
  };
  const fetchHtml = async ( templateName ) =>
  {
    setLoading( true );
    setTimeout( async () =>
    {
      try
      {
        setEditorHtml( '' );
        const response = ( templateName === "House Rental" ? await fetch( '../../templates/House_Rental_Drafting.html' ) : await fetch( '../../templates/Sale_Deed_Drafting.html' ) ); // Adjust the path if needed
        const text = await response.text();
        const tempDiv = document.createElement( 'div' );
        tempDiv.innerHTML = text;
        setEditorHtml( '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang=""><head></head><body class="ql-editor">' + tempDiv.innerHTML + "</body></html > " );

      } catch ( error )
      {
        console.error( 'Error loading HTML file:', error );
      }
      setLoading( false );
    }, 1000 );
  };
  const sampleData = {
    createdDate: '2024-09-26T12:00:00Z',
    createdBy: 'John Doe'
  };
  return (
    <Box sx={ { flexGrow: 1, padding: 2, gap: 1 } }  >
      <Typography variant="h4" component="div" sx={ { flexGrow: 1, margin: 0, maxWidth: '100%' } }>
        Welcome, { initialUser?.names }
      </Typography>
      <Typography color="primary" size="small">
        Selected Plan: {selectedPricing?.title}
      </Typography>
      <Grid2 spacing={ 2 } container sx={ { paddingTop: 3 } }>
        <Grid2 size={ 12 }>
          <FormControl sx={ { width: 400, paddingBottom: 1 } }   >
            <DcsAutocomplete
              options={ templateTypes }
              label='Select Template Types'
              selectedValue={ selectedValue }
              width={ 300 }
              onChange={ handleChange }
            >
            </DcsAutocomplete>

            <div style={ { marginTop: 1 } }>
              { loading ? (
                <DcsPageLoader
                  message={ "Loading...." }
                  size={ 20 }
                  isCircular={ false }
                />
              ) : (
                <p  >{ loading }</p>
              ) }
            </div>
          </FormControl>
          {
            selectedValue && (
              <DcsCreatedInfo
                createdDate={ sampleData.createdDate }
                createdBy={ initialUser?.email }
              /> )
          }

        </Grid2>

        { editorHtml !== '' && (
          <>
            <Grid2 size={ 12 }>
              {/* <DcsQuillEditor
                templateName={ selectedValue.title }
                templateContent={ editorHtml } /> */}
              <RentalAgreement />

            </Grid2>
            {/* <Grid2 size={ 6 }>
              <Card raised={ true } sx={ { marginTop: 2 } }
              >
                <CardHeader title="Rendered Output" sx={ {
                  fontSize: 10,
                  fontFamily: 'inherit',
                  fontWeight: 500,
                  paddingBottom: 1,
                  paddingTop: 1
                } }>
                </CardHeader>
                <Divider></Divider>
                <CardContent>
                </CardContent>
              </Card>

            </Grid2> */}
          </>
        ) }
      </Grid2>
      {
        selectedValue && (
          <DcsConfirmationDialog
            title='Do you want to change template?'
            content='Existing data will not be recoverable.'
            open={ dialogOpen }
            onClose={ handleCloseDialog }
            onConfirm={ handleConfirm }
          />
        )
      }
    </Box>
  );
}

export default Dashboard;